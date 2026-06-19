import streamlit as st
import requests

st.set_page_config(page_title="국가 정보", page_icon="🏳️", layout="centered")

API_BASE = "https://api.restcountries.com/countries/v5"
API_KEY = "rc_live_9607ffca4e274b0e9a61970e78032b77"  # 발급받은 본인 키

# 🔥 한국어 도시 이름과 영문 이름 모두 대응할 수 있도록 수정
CITY_TO_CODE = {
    "서울": "KR", "부산": "KR", "제주": "KR", "Seoul": "KR",
    "Paris": "FR", "Lyon": "FR", "Nice": "FR",
    "Tokyo": "JP", "Osaka": "JP", "Kyoto": "JP",
    "New York": "US", "Los Angeles": "US", "San Francisco": "US",
    "London": "GB", "Manchester": "GB", "Edinburgh": "GB"
}

# 🔥 app.py에 기재된 모든 도시를 완벽히 커버할 수 있도록 내장(FALLBACK) 데이터 확장
FALLBACK = {
    "서울": {"name": "대한민국", "flag": "https://flagcdn.com/w320/kr.png", "capital": "서울", "population": 51780000, "currency": "KRW", "language": "한국어"},
    "부산": {"name": "대한민국", "flag": "https://flagcdn.com/w320/kr.png", "capital": "서울", "population": 51780000, "currency": "KRW", "language": "한국어"},
    "제주": {"name": "대한민국", "flag": "https://flagcdn.com/w320/kr.png", "capital": "서울", "population": 51780000, "currency": "KRW", "language": "한국어"},
    "Seoul": {"name": "대한민국", "flag": "https://flagcdn.com/w320/kr.png", "capital": "서울", "population": 51780000, "currency": "KRW", "language": "한국어"},
    
    "Paris": {"name": "France", "flag": "https://flagcdn.com/w320/fr.png", "capital": "Paris", "population": 67390000, "currency": "EUR", "language": "French"},
    "Lyon": {"name": "France", "flag": "https://flagcdn.com/w320/fr.png", "capital": "Paris", "population": 67390000, "currency": "EUR", "language": "French"},
    "Nice": {"name": "France", "flag": "https://flagcdn.com/w320/fr.png", "capital": "Paris", "population": 67390000, "currency": "EUR", "language": "French"},
    
    "Tokyo": {"name": "Japan", "flag": "https://flagcdn.com/w320/jp.png", "capital": "Tokyo", "population": 125800000, "currency": "JPY", "language": "Japanese"},
    "Osaka": {"name": "Japan", "flag": "https://flagcdn.com/w320/jp.png", "capital": "Tokyo", "population": 125800000, "currency": "JPY", "language": "Japanese"},
    "Kyoto": {"name": "Japan", "flag": "https://flagcdn.com/w320/jp.png", "capital": "Tokyo", "population": 125800000, "currency": "JPY", "language": "Japanese"},
    
    "New York": {"name": "United States", "flag": "https://flagcdn.com/w320/us.png", "capital": "Washington D.C.", "population": 331900000, "currency": "USD", "language": "English"},
    "Los Angeles": {"name": "United States", "flag": "https://flagcdn.com/w320/us.png", "capital": "Washington D.C.", "population": 331900000, "currency": "USD", "language": "English"},
    "San Francisco": {"name": "United States", "flag": "https://flagcdn.com/w320/us.png", "capital": "Washington D.C.", "population": 331900000, "currency": "USD", "language": "English"},
    
    "London": {"name": "United Kingdom", "flag": "https://flagcdn.com/w320/gb.png", "capital": "London", "population": 67330000, "currency": "GBP", "language": "English"},
    "Manchester": {"name": "United Kingdom", "flag": "https://flagcdn.com/w320/gb.png", "capital": "London", "population": 67330000, "currency": "GBP", "language": "English"},
    "Edinburgh": {"name": "United Kingdom", "flag": "https://flagcdn.com/w320/gb.png", "capital": "London", "population": 67330000, "currency": "GBP", "language": "English"},
}

@st.cache_data
def get_country_info(code):
    """ISO alpha-2 코드로 REST Countries v5에서 국가 정보를 받아온다. 실패 시 None."""
    try:
        url = f"{API_BASE}/codes.alpha_2/{code}"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        items = data.get("data", {}).get("objects", [])
        if not items:
            return None
        c = items[0]

        currencies = c.get("currencies") or []
        languages = c.get("languages") or []
        capitals = c.get("capitals") or []
        return {
            "name": c.get("names", {}).get("common", code),
            "flag": c.get("flag", {}).get("url_png", ""),
            "capital": capitals[0].get("name", "정보 없음") if capitals else "정보 없음",
            "population": c.get("population", 0),
            "currency": ", ".join(cur.get("code", "") for cur in currencies) or "정보 없음",
            "language": ", ".join(lang.get("name", "") for lang in languages) or "정보 없음",
        }
    except Exception:
        return None

st.title("🏳️ 국가 정보")
city = st.session_state.get("selected_city")

if not city:
    st.warning("메인 화면에서 먼저 도시를 선택해 주세요.")
else:
    st.write(f"선택한 도시: **{city}**")
    code = CITY_TO_CODE.get(city)

    info = get_country_info(code) if code else None
    source = "REST Countries v5 API"
    if info is None or not info.get("name"):
        info = FALLBACK.get(city)
        source = "내장 데이터 (API 응답 없음)"

    if info is None:
        st.error(f"'{city}'의 국가 정보를 찾지 못했습니다.")
    else:
        if info.get("flag"):
            st.image(info["flag"], width=200)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("국가", info["name"])
            st.metric("수도", info["capital"])
            st.metric("통화", info["currency"])
        with col2:
            st.metric("인구", f'{info["population"]:,}')
            st.metric("언어", info["language"])
        st.markdown("---")
        st.caption(f"출처: {source}")