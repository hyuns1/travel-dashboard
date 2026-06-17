import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="위치 지도", page_icon="🗺️", layout="wide")

st.title("🗺️ 목적지 위치 지도")

# 세션 상태에서 도시 및 좌표 가져오기
city = st.session_state.get("selected_city")
lat = st.session_state.get("latitude")
lon = st.session_state.get("longitude")

if not city or lat is None or lon is None:
    st.warning("메인 화면에서 먼저 도시를 선택해 주세요.")
else:
    st.write(f"현재 **{city}**의 중심 좌표를 지도로 표시합니다. (좌표: {lat}, {lon})")
    st.markdown("---")
    
    # 1. folium 지도 객체 생성 (선택한 도시 좌표 중심)
    m = folium.Map(location=[lat, lon], zoom_start=12, control_scale=True)
    
    # 2. 지도에 마커 추가
    folium.Marker(
        [lat, lon],
        popup=f"<b>{city}</b>",
        tooltip=city,
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)
    
    # 3. 스트림릿 화면에 지도 렌더링
    st_folium(m, width="100%", height=550)