import streamlit as st
import requests

st.set_page_config(page_title="환율 계산", page_icon="💱", layout="centered")

@st.cache_data
def get_rate(base, target):
    if base == target:
        return 1.0
    try:
        url = "https://api.frankfurter.app/latest"
        params = {"from": base, "to": target}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["rates"][target]
    except Exception:
        return None

st.title("💱 환율 계산")

# [연동 로직] 메인에서 선택된 도시의 통화를 가져옴 (없으면 USD 기본)
target_currency = st.session_state.get("currency", "USD")
city = st.session_state.get("selected_city", "선택 안 됨")

st.write(f"현재 선택된 도시 **{city}**의 통화인 **{target_currency}** 기준으로 자동 세팅되었습니다.")

currencies = ["KRW", "USD", "JPY", "EUR", "GBP"]

amount = st.number_input("금액", min_value=0.0, value=1000.0, step=100.0)
col1, col2 = st.columns(2)

with col1:
    # 한국에서 여행 가는 기준이 많으므로 기본 기준 통화는 KRW(index=0)
    base = st.selectbox("기준 통화", currencies, index=0)
with col2:
    # 메인에서 넘어온 통화가 목록에 있으면 그걸 자동으로 선택하도록 index 설정
    default_index = currencies.index(target_currency) if target_currency in currencies else 1
    target = st.selectbox("대상 통화", currencies, index=default_index)

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