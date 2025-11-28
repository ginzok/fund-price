import json
import os
import urllib.request
import urllib.error
import time

# Configuration
FUNDS_FILE = 'funds.json'
DATA_DIR = 'data'
BASE_URL = "https://developer.am.mufg.jp/fund_information_latest/fund_cd/"

def load_funds():
    if not os.path.exists(FUNDS_FILE):
        print(f"Error: {FUNDS_FILE} not found at {os.path.abspath(FUNDS_FILE)}")
        return []
    with open(FUNDS_FILE, 'r') as f:
        return json.load(f)

def fetch_fund_data(fund_code):
    url = f"{BASE_URL}{fund_code}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return json.loads(response.read().decode('utf-8'))
            else:
                print(f"Failed to fetch {fund_code}: HTTP {response.status}")
                return None
    except urllib.error.URLError as e:
        print(f"Error fetching {fund_code}: {e}")
        return None

def save_data(fund_code, data):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    file_path = os.path.join(DATA_DIR, f"{fund_code}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved data for {fund_code} to {file_path}")

def main():
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created directory: {DATA_DIR}")

    funds = load_funds()
    if not funds:
        print("No funds to process.")
        return

    for fund_code in funds:
        print(f"Processing fund: {fund_code}")
        data = fetch_fund_data(fund_code)
        if data:
            save_data(fund_code, data)
        time.sleep(1) # Be polite to the API

if __name__ == "__main__":
    main()
