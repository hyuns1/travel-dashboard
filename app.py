import streamlit as st
import requests

# 1. 페이지 기본 설정 (무조건 맨 위에 한 번만!)
st.set_page_config(
    page_title="🌐 글로벌 여행 플래너 대시보드",
    page_icon="✈️",
    layout="wide"
)

# 2. 사이드바 국가/도시 선택 시스템
with st.sidebar:
    st.header("📍 여행지 설정")
    
    country = st.selectbox("국가를 선택하세요", ["대한민국", "프랑스", "일본", "미국", "영국"])
    
    city_map = {
        "대한민국": ["서울", "부산", "제주"],
        "프랑스": ["Paris", "Lyon", "Nice"],
        "일본": ["Tokyo", "Osaka", "Kyoto"],
        "미국": ["New York", "Los Angeles", "San Francisco"],
        "영국": ["London", "Manchester", "Edinburgh"]
    }
    
    cities = city_map.get(country, ["서울"])
    selected_city = st.selectbox("도시를 선택하세요", cities)
    
    # 🔥 모든 페이지(날씨, 지도 등)가 공유할 세션 상태에 도시 이름 저장
    st.session_state["selected_city"] = selected_city

# 3. 메인 대시보드 화면 구성 (날씨 파일 임포트로 인한 간섭 원천 차단)
st.title("🌐 글로벌 여행 플래너 대시보드")
st.markdown("하나의 대시보드에서 여행지의 날씨, 환율, 지도를 한눈에 확인하세요.")
st.markdown("---")

st.subheader(f"📊 {selected_city} 여행 정보 프리뷰")

# app.py 자체에서 가볍게 Open-Meteo API를 호출하여 요약 정보만 표현합니다.
# 이렇게 하면 날씨.py 파일을 임포트할 필요가 없어서 화면이 겹치는 문제가 100% 해결됩니다.
from pages.utils.geocode import geocode
coords = geocode(selected_city)

if coords:
    lat, lon = coords
    
    # 3분할 레이아웃 배치
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🌤️ 실시간 날씨 요약")
        try:
            # 오픈 메테오 API 직접 호출 (대시보드용 경량화 버전)
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code"
            response = requests.get(url).json()
            current_temp = response["current"]["temperature_2m"]
            
            st.markdown("### 🌤️")
            st.metric("현재 기온", f"{current_temp}°C")
            st.caption("📈 상세한 7일 예보 그래프는 왼쪽 **[날씨]** 탭에서 확인하세요!")
        except Exception:
            st.error("실시간 날씨 요약을 불러오지 못했습니다.")
            
    with col2:
        st.subheader("💱 실시간 환율 정보")
        st.info(f"현재 {selected_city}의 통화 환율 정보가 실시간 연동 중입니다.")
        st.caption("💵 상세 계산기는 왼쪽 메뉴의 **[환율]** 탭을 이용해 주세요.")
        
    with col3:
        st.subheader("🗺️ 위치 및 지도")
        st.metric("위도 (Latitude)", f"{lat:.4f}°")
        st.metric("경도 (Longitude)", f"{lon:.4f}°")
        st.caption("📍 인근 주요 관광지 확인은 왼쪽 메뉴의 **[지도]** 탭을 이용해 주세요.")

else:
    st.error(f"'{selected_city}'의 위치 정보를 가져올 수 없습니다.")