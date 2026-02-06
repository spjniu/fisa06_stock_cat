import FinanceDataReader as fdr
import requests
import os
import math  # nan 체크용
from datetime import datetime, timedelta

def get_stock_data(symbol):
    """주가 데이터와 등락률 반환 (에러 처리 강화)"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=10) # 넉넉하게
        
        df = fdr.DataReader(symbol, start_date)
        
        # 데이터가 비어있거나 너무 적을 경우 방어 코드
        if len(df) < 2:
            return 0, 0 

        # 결측치(NaN)가 있으면 앞의 값으로 채움 (ffill)
        df = df.fillna(method='ffill')

        today_close = df.iloc[-1]['Close']
        yesterday_close = df.iloc[-2]['Close']
        
        # 0으로 나누기 방지
        if yesterday_close == 0:
            return today_close, 0

        change_rate = ((today_close - yesterday_close) / yesterday_close) * 100
        
        # 만약 계산 결과가 nan이면 0으로 처리
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

def format_price(price):
    """가격 포맷팅 (쉼표 추가)"""
    if math.isnan(price): return "Error"
    return f"{price:,.0f} KRW"

def format_rate(rate):
    """등락률 포맷팅 (색상 이모지 + 퍼센트)"""
    if math.isnan(rate): return "0.00%"
    
    if rate > 0:
        return f"🔴 +{rate:.2f}%" # 상승
    elif rate < 0:
        return f"🔵 {rate:.2f}%"  # 하락 (마이너스는 숫자에 포함됨)
    else:
        return f"➖ 0.00%"       # 보합

def update_readme():
    # 1. 데이터 가져오기
    samsung_price, samsung_change = get_stock_data('005930') 
    btc_price, btc_change = get_stock_data('BTC/KRW')       
    
    # 2. 시장 분위기 판단
    market_mood_good = (samsung_change + btc_change) > 0
    
    # 3. 멘트 선정
    if market_mood_good:
        cat_message = "🚀 떡상 가즈아! 츄르 파티다! (시장 좋음)"
        cat_emoji = "😻"
    else:
        cat_message = "📉 존버는 승리한다... (시장 나쁨)"
        cat_emoji = "😿"

    cat_url = get_cat_image(market_mood_good)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 4. README 작성 (표 칸을 3개로 정확히 나눔!)
    content = f"""
# {cat_emoji} 금융 고양이 대시보드 (Finance Cat)

### {cat_message}

| 종목 | 현재가 | 등락률 |
| :--- | :---: | :---: |
| **삼성전자** | {format_price(samsung_price)} | {format_rate(samsung_change)} |
| **비트코인** | {format_price(btc_price)} | {format_rate(btc_change)} |

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
