import requests
from time import sleep

HEADERS = {
    "User-Agent": "...",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/option-chain",
    "Connection": "keep-alive",
    "Origin": "https://www.nseindia.com",
    "sec-ch-ua": '"Google Chrome";v="115", "Chromium";v="115", "Not)A;Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
}

def fetch_nifty_oi():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        # Step 1: Get cookies from homepage
        response = session.get("https://www.nseindia.com", timeout=10)
        if response.status_code != 200:
            print(f"Homepage request failed with {response.status_code}")
            return []

        sleep(2)  # Wait 2 seconds before the API call

        # Step 2: Request the option chain data with session and cookies
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('records', {}).get('data', [])
        else:
            print(f"Failed to fetch data, status code: {response.status_code}")
            return []

    except Exception as e:
        print("Exception during fetch:", e)
        return []
