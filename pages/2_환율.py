import streamlit as st
import requests

# 페이지 기본 설정 (반드시 다른 st 명령보다 먼저, 맨 위에)
st.set_page_config(page_title="환율 계산", page_icon="💱", layout="centered")


@st.cache_data
def get_rate(base, target):
    """기준 통화에서 대상 통화로의 환율 1개를 Frankfurter API에서 받아온다."""
    # 같은 통화면 환율은 1
    if base == target:
        return 1.0
    try:
        url = "https://api.frankfurter.app/latest"
        params = {"from": base, "to": target}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        # 응답의 rates 딕셔너리에서 대상 통화 값을 꺼낸다
        return data["rates"][target]
    except Exception:
        # 네트워크 실패 등 문제가 생기면 None 반환
        return None


# 화면 제목
st.title("💱 환율 계산")
st.write("금액과 통화를 선택하면 환산 결과를 보여줍니다.")

# 사용할 통화 목록
currencies = ["KRW", "USD", "JPY", "EUR", "GBP"]

# 입력 영역
amount = st.number_input("금액", min_value=0.0, value=1000.0, step=100.0)
col1, col2 = st.columns(2)
with col1:
    base = st.selectbox("기준 통화", currencies, index=0)
with col2:
    target = st.selectbox("대상 통화", currencies, index=1)

# 버튼을 누르면 환산
if st.button("환산하기"):
    rate = get_rate(base, target)
    if rate is None:
        st.error("환율을 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.")
    else:
        result = amount * rate
        st.metric(
            label=f"{amount:,.0f} {base} →",
            value=f"{result:,.2f} {target}",
        )
        st.caption(f"적용 환율: 1 {base} = {rate} {target}")