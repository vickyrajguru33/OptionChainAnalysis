import schedule
import time
from oi_fetcher import fetch_nifty_oi
from db_handler import insert_oi_data
from rich.console import Console
from rich.table import Table

console = Console()

def job():
    data = fetch_nifty_oi()
    if data:
        insert_oi_data(data)
        show_summary(data)

def show_summary(data):
    table = Table(title="NIFTY Open Interest Snapshot")
    table.add_column("Strike", justify="right")
    table.add_column("CE OI", justify="right")
    table.add_column("PE OI", justify="right")

    for item in data[:10]:  # show first 10 for brevity
        strike = str(item.get('strikePrice'))
        ce_oi = str(item.get('CE', {}).get('openInterest', 0))
        pe_oi = str(item.get('PE', {}).get('openInterest', 0))
        table.add_row(strike, ce_oi, pe_oi)

    console.clear()
    console.print(table)

def start_scheduler():
    schedule.every(5).minutes.do(job)
    job()  # run immediately
    while True:
        schedule.run_pending()
        time.sleep(1)
