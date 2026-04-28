import requests
import pandas as pd
import sqlite3
import json
import os
import time

def fetch_nemo_page(page_index):
    """
    특정 페이지의 Nemo API 데이터를 수집합니다.
    """
    url = "https://www.nemoapp.kr/api/store/search-list"
    params = {
        "Subway": "222",
        "Radius": "1000",
        "CompletedOnly": "false",
        "NELat": "37.50743127473891",
        "NELng": "127.04840715411191",
        "SWLat": "37.47824757652681",
        "SWLng": "127.01524006108677",
        "Zoom": "15",
        "SortBy": "29",
        "PageIndex": str(page_index)
    }
    headers = {
        "referer": "https://www.nemoapp.kr/store",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    }

    print(f"Calling API Page {page_index}...")
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            return items
        else:
            print(f"Error fetching page {page_index}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception on page {page_index}: {e}")
        return None

def fetch_all_nemo_data():
    """
    데이터가 없을 때까지 모든 페이지를 수집합니다.
    """
    all_items = []
    page_index = 0
    
    while True:
        items = fetch_nemo_page(page_index)
        
        if items is None:
            print("Stopping due to error.")
            break
            
        if not items:
            print("No more items found. Finished collection.")
            break
            
        print(f"Collected {len(items)} items from page {page_index}.")
        all_items.extend(items)
        
        page_index += 1
        time.sleep(1) # 1초 지연
        
    return all_items

def save_to_sqlite(items, db_path):
    """
    수집된 데이터를 SQLite 데이터베이스에 저장합니다.
    """
    if not items:
        print("No items to save.")
        return

    # 데이터 프레임으로 변환
    df = pd.DataFrame(items)

    # 리스트나 딕셔너리 형태의 컬럼을 JSON 문자열로 변환
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
            df[col] = df[col].apply(lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (list, dict)) else x)

    # DB 연결 및 저장
    conn = sqlite3.connect(db_path)
    try:
        # 기존 테이블이 있으면 덮어쓰기
        df.to_sql("nemo_stores", conn, if_exists="replace", index=False)
        print(f"Successfully saved {len(df)} records to {db_path} in 'nemo_stores' table.")
    finally:
        conn.close()

if __name__ == "__main__":
    # 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    DB_PATH = os.path.join(DATA_DIR, "nemo_data.db")

    # 모든 데이터 수집
    all_collected_items = fetch_all_nemo_data()

    # 데이터 저장
    if all_collected_items:
        save_to_sqlite(all_collected_items, DB_PATH)
    else:
        print("Data collection yielded no results.")
