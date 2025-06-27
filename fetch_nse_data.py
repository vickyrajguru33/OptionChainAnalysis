from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

def fetch_nse_option_chain():
    options = Options()
    options.headless = True  # run Chrome in headless mode
    driver = webdriver.Chrome(options=options)

    # Open NSE homepage to get cookies
    driver.get("https://www.nseindia.com")

    # Extract cookies from Selenium session
    selenium_cookies = driver.get_cookies()

    # Format cookies for requests
    cookie_jar = requests.cookies.RequestsCookieJar()
    for cookie in selenium_cookies:
        cookie_jar.set(cookie['name'], cookie['value'])

    session = requests.Session()
    session.cookies = cookie_jar

    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/option-chain",
        "Connection": "keep-alive",
        "Origin": "https://www.nseindia.com",
    }

    response = session.get(url, headers=headers, timeout=10)

    driver.quit()

    if response.status_code == 200:
        return response.json().get('records', {}).get('data', [])
    else:
        print(f"Failed to fetch data, status code: {response.status_code}")
        return []
