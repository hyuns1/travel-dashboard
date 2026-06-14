import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="🧳 여행 플래너 대시보드",
    page_icon="🗺️",
    layout="wide"
)

# 2. 세션 상태(st.session_state) 초기화
# 다른 페이지(날씨, 지도, 환율 등)에서 이 값을 참조하여 동작합니다.
if "selected_city" not in st.session_state:
    st.session_state["selected_city"] = ""
if "latitude" not in st.session_state:
    st.session_state["latitude"] = None
if "longitude" not in st.session_state:
    st.session_state["longitude"] = None

# 3. 메인 화면 UI 디자인
st.title("🧳 여행 플래너 대시보드")
st.markdown("---")

st.subheader("📍 여행할 도시를 선택해 주세요")
st.write("선택하신 도시의 날씨, 환율, 국가 정보 및 지도가 각 탭(페이지)에 자동으로 연동됩니다.")

# 테스트용 주요 도시 리스트 (우선 선택형이나 입력형으로 구현)
city_list = ["선택하세요", "Seoul", "Paris", "Tokyo", "New York", "London"]
search_city = st.selectbox("도시 선택", city_list)

# 4. 도시 선택 시 세션 상태 업데이트 및 전 페이지 공유 토대
if search_city != "선택하세요":
    st.session_state["selected_city"] = search_city
    
    # [💡 중요] Day 1 오후에 팀원 A가 utils/geocode.py를 완성하면 
    # 여기에 geocode 함수를 불러와 위경도 값을 넣어줄 예정입니다.
    # 예시 임시 값 (우선 서울 기준으로 테스트용 세팅)
    if search_city == "Seoul":
        st.session_state["latitude"] = 37.5665
        st.session_state["longitude"] = 126.9780
    
    st.success(f"🎉 **{search_city}**가 선택되었습니다! 왼쪽 사이드바의 페이지들을 확인해 보세요.")

# 5. 현재 선택된 정보 디버깅용 시각화 (개발 중 확인용)
st.sidebar.markdown("### ⚙️ 현재 전역 세션 상태")
st.sidebar.write(f"**선택된 도시:** {st.session_state['selected_city']}")
st.sidebar.write(f"**위도(Lat):** {st.session_state['latitude']}")
st.sidebar.write(f"**경도(Lon):** {st.session_state['longitude']}")
