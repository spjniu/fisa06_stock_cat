import FinanceDataReader as fdr
import requests
import os
from datetime import datetime

def get_stock_data():
    """삼성전자(005930)와 비트코인(BTC/KRW) 가격 가져오기"""
    # 삼성전자
    samsung = fdr.DataReader('005930').iloc[-1]
    # 비트코인 (Upbit 기준)
    btc = fdr.DataReader('BTC/KRW').iloc[-1]
    return samsung['Close'], btc['Close']

def get_cat_image():
    """랜덤 고양이 이미지 URL 가져오기"""
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        data = response.json()
        return data[0]['url']
    except:
        return "https://via.placeholder.com/400?text=Cat+Image+Not+Found"

def update_readme():
    samsung_price, btc_price = get_stock_data()
    cat_url = get_cat_image()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""
# 🐱 금융 고양이 대시보드 (Finance Cat)

매일 정해진 시간에 주가와 고양이를 배달해 드립니다!

### 💰 오늘의 시세
* **삼성전자**: {samsung_price:,.0f} KRW
* **비트코인**: {btc_price:,.0f} KRW

### 📸 오늘의 힐링 고양이
![Random Cat]({cat_url})

---
⏳ 마지막 업데이트: {now} (KST)
*본 리포지토리는 GitHub Actions를 통해 자동화되었습니다.*
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()