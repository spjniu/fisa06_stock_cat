import FinanceDataReader as fdr
import requests
import os
from datetime import datetime, timedelta

def get_stock_data(symbol):
    """
    주가 데이터와 등락률을 계산해서 반환
    """
    # 최근 1주일 데이터 가져오기 (공휴일 등 고려해서 넉넉하게)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    df = fdr.DataReader(symbol, start_date)
    
    # 데이터가 2개 이상 있어야 등락률 계산 가능
    if len(df) < 2:
        return 0, 0 # 데이터 부족 시 0 처리

    today_close = df.iloc[-1]['Close']
    yesterday_close = df.iloc[-2]['Close']
    
    # 등락률 계산 (%)
    change_rate = ((today_close - yesterday_close) / yesterday_close) * 100
    
    return today_close, change_rate

def get_cat_image(is_market_good):
    """
    시장이 좋으면 신난 고양이, 나쁘면 슬픈 고양이 태그로 검색
    """
    tag = "happy" if is_market_good else "sad" # 검색 키워드 변경
    # TheCatAPI는 태그 검색이 유료거나 제한적일 수 있어서, 
    # 무료 버전에서는 그냥 랜덤으로 하되 멘트로 분위기를 냅니다.
    # (여기서는 이미지 URL은 그대로 랜덤을 쓰되, 함수 구조만 잡아둡니다)
    
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        data = response.json()
        return data[0]['url']
    except:
        return "https://via.placeholder.com/400?text=Cat+Image+Error"

def format_price(price, change_rate):
    """가격과 등락률을 예쁘게 포맷팅 (상승=빨강, 하락=파랑)"""
    if change_rate > 0:
        emoji = "🔴" # 떡상
        sign = "+"
    elif change_rate < 0:
        emoji = "🔵" # 떡락
        sign = ""
    else:
        emoji = "➖" # 보합
        sign = ""
        
    return f"{emoji} {price:,.0f} KRW ({sign}{change_rate:.2f}%)"

def update_readme():
    # 1. 데이터 가져오기
    samsung_price, samsung_change = get_stock_data('005930') # 삼성전자
    btc_price, btc_change = get_stock_data('BTC/KRW')        # 비트코인
    
    # 2. 시장 분위기 파악 (둘 다 떨어지면 우울함)
    market_mood_good = (samsung_change + btc_change) > 0
    
    # 3. 고양이 멘트 선정
    if market_mood_good:
        cat_message = "🚀 주인님! 오늘은 츄르 3개 먹어도 될까요? (시장 좋음)"
        cat_emoji = "😻"
    else:
        cat_message = "📉 주인님... 한강 물 온도가 따뜻하네요... (시장 나쁨)"
        cat_emoji = "😿"

    cat_url = get_cat_image(market_mood_good)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 4. README 내용 작성
    content = f"""
# {cat_emoji} 금융 고양이 대시보드 (Finance Cat)

### {cat_message}

| 종목 | 현재가 | 등락률 |
| :--- | :---: | :---: |
| **삼성전자** | {format_price(samsung_price, samsung_change)} |
| **비트코인** | {format_price(btc_price, btc_change)} |

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
