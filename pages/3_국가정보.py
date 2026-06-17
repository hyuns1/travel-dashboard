import streamlit as st
import requests

st.set_page_config(page_title="국가 정보", page_icon="🏳️", layout="centered")

API_BASE = "https://api.restcountries.com/countries/v5"
API_KEY = "여기에_본인_키"  # 발급받은 본인 키

# 도시 -> ISO alpha-2 국가 코드
CITY_TO_CODE = {
    "Seoul": "KR", "Paris": "FR", "Tokyo": "JP",
    "New York": "US", "London": "GB",
}

FALLBACK = {
    "Seoul": {"name": "대한민국", "flag": "https://flagcdn.com/w320/kr.png",
              "capital": "서울", "population": 51780000, "currency": "KRW", "language": "한국어"},
    "Paris": {"name": "France", "flag": "https://flagcdn.com/w320/fr.png",
              "capital": "Paris", "population": 67390000, "currency": "EUR", "language": "French"},
    "Tokyo": {"name": "Japan", "flag": "https://flagcdn.com/w320/jp.png",
              "capital": "Tokyo", "population": 125800000, "currency": "JPY", "language": "Japanese"},
    "New York": {"name": "United States", "flag": "https://flagcdn.com/w320/us.png",
                 "capital": "Washington D.C.", "population": 331900000, "currency": "USD", "language": "English"},
    "London": {"name": "United Kingdom", "flag": "https://flagcdn.com/w320/gb.png",
               "capital": "London", "population": 67330000, "currency": "GBP", "language": "English"},
}


@st.cache_data
def get_country_info(code):
    """ISO alpha-2 코드로 REST Countries v5에서 국가 정보를 받아온다. 실패 시 None."""
    try:
        # 경로로 정확히 조회: /codes.alpha_2/KR
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
        st.caption(f"출처: {source}")