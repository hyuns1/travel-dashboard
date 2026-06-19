"""
utils/geocode.py
-----------------
도시명을 위도/경도로 변환하는 공용 지오코딩 유틸리티.

- Nominatim(OpenStreetMap) API 사용 → 무료, API 키 불필요
- Nominatim 사용 정책 준수: 요청 간 최소 1초 간격 유지, User-Agent 헤더 필수
- 같은 도시를 반복 조회할 때 API를 또 호출하지 않도록 메모리 캐시 + 파일 캐시 사용
  (팀원들이 같이 쓰는 "공용" 모듈이라 캐시 파일을 같이 커밋하면 다음부터는 API 호출 자체가 줄어듦)

사용 예:
    from utils.geocode import geocode, geocode_many

    geocode("서울")                       # (37.5666791, 126.9782914)
    geocode("Paris", country_code="fr")   # 프랑스로 검색 범위 한정
    geocode_many(["서울", "부산", "대전"]) # {"서울": (..), "부산": (..), "대전": (..)}
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests

# ---------------------------------------------------------------------------
# 설정값
# ---------------------------------------------------------------------------

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# Nominatim 사용 정책상 User-Agent는 필수입니다.
# 실제 배포 전에는 본인/팀의 연락처(이메일 또는 깃허브 등)로 바꿔주세요.
USER_AGENT = "travel-dashboard/1.0 (+https://github.com/hyuns1/travel-dashboard)"

MIN_REQUEST_INTERVAL = 1.0  # 초 단위. Nominatim 정책: 1초에 1건 이하로 요청
REQUEST_TIMEOUT = 5  # 초 단위

CACHE_FILE = Path(__file__).parent / "geocode_cache.json"

# ---------------------------------------------------------------------------
# 내부 상태 (캐시 / 마지막 요청 시각)
# ---------------------------------------------------------------------------

_last_request_time: float = 0.0


def _load_disk_cache() -> Dict[str, Optional[Tuple[float, float]]]:
    """디스크에 저장된 캐시 파일을 읽어서 메모리로 불러옵니다."""
    if not CACHE_FILE.exists():
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        # JSON에는 튜플이 없어서 리스트로 저장되므로 다시 튜플로 변환
        return {k: (tuple(v) if v is not None else None) for k, v in raw.items()}
    except (json.JSONDecodeError, OSError):
        return {}


def _save_disk_cache(cache: Dict[str, Optional[Tuple[float, float]]]) -> None:
    """현재 캐시를 디스크에 저장합니다. 실패해도 프로그램이 멈추지 않도록 조용히 무시합니다."""
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


# 모듈이 처음 import될 때 디스크 캐시를 메모리로 한 번 로드
_memory_cache: Dict[str, Optional[Tuple[float, float]]] = _load_disk_cache()


def _respect_rate_limit() -> None:
    """직전 요청과의 간격이 MIN_REQUEST_INTERVAL보다 짧으면 그만큼 대기합니다."""
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - elapsed)
    _last_request_time = time.time()


def _cache_key(city_name: str, country_code: Optional[str]) -> str:
    return f"{city_name.strip().lower()}|{(country_code or '').lower()}"


# ---------------------------------------------------------------------------
# 공개 함수
# ---------------------------------------------------------------------------

def geocode(
    city_name: str,
    country_code: Optional[str] = None,
    use_cache: bool = True,
) -> Optional[Tuple[float, float]]:
    """
    도시명을 (위도, 경도) 튜플로 변환합니다.

    Args:
        city_name: 변환할 도시명. 한글/영문 모두 가능 (예: "서울", "Paris", "New York")
        country_code: ISO 3166-1 alpha-2 국가 코드로 검색 범위를 제한 (예: "kr", "fr").
                       동명의 도시가 여러 나라에 있을 때 정확도를 높이는 용도.
        use_cache: True이면 캐시에 있는 결과를 먼저 사용 (기본값 True, 보통 그대로 두면 됨)

    Returns:
        (lat, lon) 튜플. 검색 결과가 없으면 None.

    Example:
        >>> geocode("서울")
        (37.5666791, 126.9782914)
    """
    if not city_name or not city_name.strip():
        return None

    key = _cache_key(city_name, country_code)

    if use_cache and key in _memory_cache:
        return _memory_cache[key]

    params = {
        "q": city_name,
        "format": "json",
        "limit": 1,
    }
    if country_code:
        params["countrycodes"] = country_code

    headers = {"User-Agent": USER_AGENT}

    _respect_rate_limit()

    try:
        resp = requests.get(
            NOMINATIM_URL, params=params, headers=headers, timeout=REQUEST_TIMEOUT
        )
        resp.raise_for_status()
        results = resp.json()
    except (requests.RequestException, ValueError) as e:
        print(f"[geocode] 요청 실패: '{city_name}' ({e})")
        return None

    if not results:
        result: Optional[Tuple[float, float]] = None
    else:
        result = (float(results[0]["lat"]), float(results[0]["lon"]))

    _memory_cache[key] = result
    _save_disk_cache(_memory_cache)

    return result


def geocode_many(
    city_names: List[str],
    country_code: Optional[str] = None,
) -> Dict[str, Optional[Tuple[float, float]]]:
    """
    여러 도시명을 한 번에 위경도로 변환합니다.
    (내부적으로 geocode()를 순서대로 호출 — 캐시에 없는 도시만 실제 요청이 발생)

    Args:
        city_names: 도시명 리스트
        country_code: 모든 도시에 동일하게 적용할 국가 코드

    Returns:
        {도시명: (lat, lon) 또는 None} 딕셔너리
    """
    return {name: geocode(name, country_code=country_code) for name in city_names}


def clear_cache() -> None:
    """메모리 + 디스크 캐시를 모두 비웁니다. 테스트하거나 잘못된 결과를 갱신하고 싶을 때 사용."""
    _memory_cache.clear()
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()


# ---------------------------------------------------------------------------
# 모듈 단독 실행 시 간단한 동작 테스트
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_cities = ["서울", "부산", "Paris", "Nonexistent City Name 12345"]
    for city in test_cities:
        coord = geocode(city)
        print(f"{city}: {coord}")
