import FinanceDataReader as fdr
import requests
import os
import math
from datetime import datetime, timedelta

def get_stock_data(symbol):
    """주가 데이터와 등락률 반환 (에러 처리 강화)"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=10)
        
        # 데이터 가져오기
        df = fdr.DataReader(symbol, start_date)
        
        if len(df) < 2:
            return 0, 0 

        df = df.fillna(method='ffill') # 결측치 채움

        today_close = df.iloc[-1]['Close']
        yesterday_close = df.iloc[-2]['Close']
        
        if yesterday_close == 0:
            return today_close, 0

        change_rate = ((today_close - yesterday_close) / yesterday_close) * 100
        
        if math.isnan(change_rate):
            change_rate = 0.0
            
        return today_close, change_rate

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return 0, 0

def get_cat_image(is_market_good):
    tag = "happy" if is_market_good else "sad"
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        data = response.json()
        return data[0]['url']
    except:
        return "https://via.placeholder.com/400?text=Cat+Error"

def format_price(price, symbol):
    """가격 포맷팅 (지수는 소수점, 주식은 정수)"""
    if math.isnan(price): return "Error"
    
    # 지수(KOSPI, KOSDAQ)나 코인은 소수점이 있을 수 있음
    if symbol in ["KS11", "KQ11", "IXIC", "US500"]: 
        return f"{price:,.2f}"
    else:
        return f"{price:,.0f} KRW"

def format_rate(rate):
    """등락률 포맷팅"""
    if math.isnan(rate): return "0.00%"
    
    if rate > 0:
        return f"🔴 +{rate:.2f}%"
    elif rate < 0:
        return f"🔵 {rate:.2f}%"
    else:
        return f"➖ 0.00%"

def update_readme():
    # -------------------------------------------------------
    # ⭐ 여기에 보고 싶은 종목을 마음껏 추가하세요!
    # [종목명, 코드] 형식입니다.
    # -------------------------------------------------------
    tickers = [
        {"name": "코스피 지수", "code": "KS11"},
        {"name": "삼성전자", "code": "005930"},
        {"name": "SK하이닉스", "code": "000660"},
        {"name": "현대차", "code": "005380"},
        {"name": "POSCO홀딩스", "code": "005490"},
        {"name": "카카오", "code": "035720"},
        {"name": "비트코인", "code": "BTC/KRW"}
    ]
    
    table_rows = []
    total_change = 0 # 시장 분위기 파악용 합계

    # 반복문으로 모든 종목 데이터 가져오기
    for ticker in tickers:
        price, change = get_stock_data(ticker['code'])
        total_change += change
        
        # 표 한 줄 만들기
        row = f"| **{ticker['name']}** | {format_price(price, ticker['code'])} | {format_rate(change)} |"
        table_rows.append(row)

    # 시장 분위기 멘트 선정 (평균 등락률로 판단)
    avg_change = total_change / len(tickers)
    
    if avg_change > 0:
        cat_message = "🚀 국장이 살아나고 있어요! 가즈아! (시장 좋음)"
        cat_emoji = "😻"
        is_good = True
    else:
        cat_message = "📉 파란나라를 보았니... 꿈과 희망이... (시장 나쁨)"
        cat_emoji = "😿"
        is_good = False

    cat_url = get_cat_image(is_good)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 리스트를 문자열로 합치기
    table_body = "\n".join(table_rows)

    content = f"""
# {cat_emoji} 국장 고양이 대시보드 (K-Stock Cat)

### {cat_message}

| 종목 | 현재가 | 등락률 |
| :--- | :---: | :---: |
{table_body}

### 📸 오늘의 힐링 짤
![Random Cat]({cat_url})

---
⏳ 마지막 업데이트: {now} (KST)
*Powered by GitHub Actions & FinanceDataReader*
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()
