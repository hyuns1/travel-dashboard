import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="🌐 여행 플래너 대시보드",
    page_icon="✈️",
    layout="wide"
)

# 2. 세션 상태(st.session_state) 초기화
if "selected_city" not in st.session_state:
    st.session_state["selected_city"] = "Seoul"  # 기본값 서울

# 각 도시별 매핑 데이터 (국가 정보 및 환율 연동용)
CITY_DATA = {
    "Seoul": {"lat": 37.5665, "lon": 126.9780, "currency": "KRW"},
    "Paris": {"lat": 48.8566, "lon": 2.3522, "currency": "EUR"},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503, "currency": "JPY"},
    "New York": {"lat": 40.7128, "lon": -74.0060, "currency": "USD"},
    "London": {"lat": 51.5074, "lon": -0.1278, "currency": "GBP"}
}

# 3. 메인 화면 UI 디자인
st.title("✈️ 여행 플래너 대시보드")
st.markdown("---")

st.subheader("📍 여행할 도시를 선택해 주세요")
st.write("선택하신 도시의 날씨, 환율, 국가 정보 및 지도가 각 탭(페이지)에 자동으로 연동됩니다.")

# 도시 선택 드롭다운 (기본값 세션 상태와 연동)
cities = list(CITY_DATA.keys())
selected = st.selectbox(
    "목적지 선택", 
    cities, 
    index=cities.index(st.session_state["selected_city"])
)

# 사용자가 도시를 바꾸면 세션 상태를 즉시 업데이트
if selected != st.session_state["selected_city"]:
    st.session_state["selected_city"] = selected

# 세션 상태에 위도, 경도, 통화 정보 함께 저장
st.session_state["latitude"] = CITY_DATA[selected]["lat"]
st.session_state["longitude"] = CITY_DATA[selected]["lon"]
st.session_state["currency"] = CITY_DATA[selected]["currency"]

# 현재 상태 보여주기 대시보드
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="현재 검색된 도시", value=st.session_state["selected_city"])
with col2:
    st.metric(label="통화 단위", value=st.session_state["currency"])
with col3:
    st.metric(label="좌표", value=f"{st.session_state['latitude']}, {st.session_state['longitude']}")

st.info("💡 왼쪽 사이드바 메뉴를 클릭하시면 해당 도시의 상세 정보를 확인하실 수 있습니다!")