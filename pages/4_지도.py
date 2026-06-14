import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="지도 대시보드", page_icon="🗺️", layout="wide")

st.title("🗺️ 선택 도시 지도 정보")

# 메인(app.py)에서 도시를 선택했는지 확인
if not st.session_state.get("selected_city"):
    st.warning("⚠️ 메인 화면(app.py)에서 먼저 여행할 도시를 선택해 주세요!")
else:
    city = st.session_state["selected_city"]
    lat = st.session_state["latitude"]
    lon = st.session_state["longitude"]
    
    st.subheader(f"📍 {city}의 위치 정보")
    
    if lat and lon:
        st.write(f"위도: {lat}, 경도: {lon}")
        
        # Folium 지도 생성
        m = folium.Map(location=[lat, lon], zoom_start=12)
        folium.Marker([lat, lon], popup=city, tooltip=city).add_to(m)
        
        # 스트림릿에 지도 렌더링
        st_folium(m, width=700, height=500)
    else:
        st.error("위경도 데이터를 불러올 수 없습니다. 팀원 A의 geocode 함수 연동이 필요합니다.")
