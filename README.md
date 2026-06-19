## 팀원별 역할 및 기여도

| 팀원 | 역할 | 주요 기여 |
|------|------|-----------|
| **이현성** (팀장) | 레포 관리 / 환율·국가정보 페이지 / 발표·시연 | 환율 페이지(Frankfurter API 환산), 국가정보 페이지(REST Countries v5 연동 + API 실패 시 내장 데이터 폴백 설계), GitHub 레포 관리 및 main 브랜치 보호 설정, Streamlit Cloud 배포, 발표자료(PPT) 제작 및 발표, 시연 영상 제작 |
| **장하민** | 메인 통합 / 지도 / 공용 유틸 | `app.py` 메인 통합(`session_state` 기반 도시 전역 공유), 지도 페이지(folium 지도·마커), 공용 `geocode` 유틸(Nominatim 지오코딩, 메모리·파일 캐시, 요청 속도 제한) — 날씨·지도·메인이 공유 |
| **최진비** | 날씨 페이지 | 날씨 페이지(Open-Meteo 현재 날씨 + 7일 예보 Plotly 차트, WMO 날씨코드→이모지 매핑), 공용 geocode를 활용한 좌표 변환,도시명 -> 위경도로 변환 |



프로젝트 시연 영상 링크 (YOUTUBE)
(https://youtu.be/djEfMjl5WYA)
