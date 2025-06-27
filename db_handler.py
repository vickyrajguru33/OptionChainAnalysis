import mysql.connector
from datetime import datetime

# Connect to your SQL database
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='root',
        database='nifty_data'
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS oi_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME,
            strike_price INT,
            ce_oi BIGINT,
            pe_oi BIGINT
        )
    ''')
    conn.commit()
    conn.close()

def insert_oi_data(records):
    conn = get_connection()
    cur = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in records:
        strike = item.get('strikePrice')
        ce_oi = item.get('CE', {}).get('openInterest', 0)
        pe_oi = item.get('PE', {}).get('openInterest', 0)
        cur.execute("INSERT INTO oi_data (timestamp, strike_price, ce_oi, pe_oi) VALUES (%s, %s, %s, %s)",
                    (timestamp, strike, ce_oi, pe_oi))

    conn.commit()
    conn.close()
