import streamlit as st
import folium
from streamlit_folium import st_folium
from pages.utils.geocode import geocode

# 1. 페이지 기본 설정 (스트림릿 규칙)
st.set_page_config(page_title="여행 지도", page_icon="🗺️", layout="wide")

# 2. 세션 상태에서 메인 화면이 지정해 준 도시 이름 가져오기
city = st.session_state.get("selected_city")

# 메인 화면에서 도시를 선택하지 않고 바로 들어왔을 경우 방어 코드
if not city:
    st.warning("⚠️ 메인 화면에서 먼저 국가와 도시를 선택해 주세요.")
    st.stop()

st.title(f"🗺️ {city} 여행 지도")
st.markdown(f"**{city}**의 주요 관광지 위치와 정보를 지도를 통해 확인해 보세요.")

# 3. 공용 geocode 함수를 사용해 실시간으로 위경도 좌표 추출 (기존 CITY_DATA 딕셔너리 대체)
coords = geocode(city)

if coords is None:
    st.error(f"❌ '{city}'의 위치 정보를 가져오지 못했습니다. 도시명을 다시 확인해 주세요.")
    st.stop()

lat, lon = coords  # 변환된 위도, 경도 풀기

st.markdown("---")

# 4. Folium 지도 생성 및 마커 레이아웃 구성
# 변환된 lat, lon을 중심점으로 설정합니다.
m = folium.Map(location=[lat, lon], zoom_start=12, control_scale=True)

# 📌 [팁] 도시별 주요 관광지 마커 예시 (필요시 커스텀 가능)
# 현재는 중심점에 기본 마커 하나를 찍도록 설정되어 있습니다.
folium.Marker(
    location=[lat, lon],
    popup=f"<b>{city} 중심지</b>",
    tooltip=f"{city} 여행의 시작점!",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

# 5. 스트림릿 화면에 지도 렌더링
st_folium(m, use_container_width=True, height=550)

st.caption("지도 데이터 제공: OpenStreetMap / 지오코딩 유틸리티 연동 완료")