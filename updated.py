# 터미널에
# streamlit run main3.py

# pip install streamlit yfinance requests


import streamlit as st
import yfinance as yf
import requests

def fetch_current_price(stock_symbol):
    ticker = yf.Ticker(stock_symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0] if not todays_data.empty else None

def calculate_profit_or_loss(average_price, current_price, shares):
    total_cost = average_price * shares
    current_value = current_price * shares
    profit_or_loss = current_value - total_cost
    profit_or_loss_percentage = (profit_or_loss / total_cost) * 100
    return profit_or_loss, profit_or_loss_percentage

def get_exchange_rate():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    response = requests.get(url)
    data = response.json()
    return data['rates']['KRW']

# 스트림릿 애플리케이션 시작
st.title('주식 수익률 계산기')

# 실시간 환율 정보 가져오기
exchange_rate = get_exchange_rate()
st.write(f"## 현재 USD-KRW 환율: {int(exchange_rate):,}원")

# 주식 정보 설정
stocks = {
    'AAPL': {'average_price': 246579, 'shares': 34},
    'NVDA': {'average_price': 105981, 'shares': 60}
}

# 주식 데이터 가져오기 및 수익 계산
total_cost = 0
total_current_value = 0
profit_loss_display_data = []

for stock_symbol, info in stocks.items():
    current_price_usd = fetch_current_price(stock_symbol)
    if current_price_usd:
        current_price_krw = current_price_usd * exchange_rate
        profit_or_loss, profit_or_loss_percentage = calculate_profit_or_loss(info['average_price'], current_price_krw, info['shares'])

        # UI 출력을 위한 데이터 수집
        profit_loss_display_data.append(
            (stock_symbol, f"{stock_symbol} ({int(current_price_krw):,}원)", int(profit_or_loss), f"{profit_or_loss_percentage:.2f}%")
        )

        # 총계 계산을 위한 값 업데이트
        total_cost += info['average_price'] * info['shares']
        total_current_value += current_price_krw * info['shares']
    else:
        st.write(f"### {stock_symbol}의 가격 정보를 가져오는데 실패했습니다.")

# 수익률 메트릭 UI 구성
col1, col2, col3 = st.columns(3)
if len(profit_loss_display_data) >= 1:
    col1.metric(profit_loss_display_data[0][1], f"{profit_loss_display_data[0][2]:,}원", profit_loss_display_data[0][3])
if len(profit_loss_display_data) >= 2:
    col2.metric(profit_loss_display_data[1][1], f"{profit_loss_display_data[1][2]:,}원", profit_loss_display_data[1][3])

# 총 수익 및 손실 표시
if total_cost > 0:  # 0으로 나누는 것을 방지
    total_profit_or_loss = total_current_value - total_cost
    total_profit_or_loss_percentage = (total_profit_or_loss / total_cost) * 100
    col3.metric("TOTAL", f"{int(total_profit_or_loss):,}원", f"{total_profit_or_loss_percentage:.2f}%")
else:
    st.write("## 총계산 정보가 충분하지 않습니다.")

