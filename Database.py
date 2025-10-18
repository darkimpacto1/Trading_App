import sqlite3
import pandas as pd

# --- STEP 1: Load CSVs ---
df_companies = pd.read_csv("company_info.csv")
df_prices = pd.read_csv("stock_price_history.csv")

# ✅ Rename columns to match DB schema
df_companies.rename(columns={
    "Id": "id",
    "Ticker": "ticket",
    "Name": "company_name",
    "Sector": "sector",
    "Industry": "industry",
    "Ceo":"ceo"

}, inplace=True)

df_prices.rename(columns={
    "Id": "id",
    "Ticker": "ticket",
    "Date": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume"
}, inplace=True)

# --- STEP 2: Setup SQLite ---
conn = sqlite3.connect("stocks.db")
cursor = conn.cursor()

# Drop and recreate tables
cursor.execute("DROP TABLE IF EXISTS company")
cursor.execute("DROP TABLE IF EXISTS stock")

# ✅ Updated schema for extra columns
cursor.execute('''
CREATE TABLE company (
    id INTEGER PRIMARY KEY,
    ticket TEXT UNIQUE,
    company_name TEXT,
    sector TEXT,
    industry TEXT,
    ceo TEXT,
    Employees TEXT,
    Website TEXT
)
''')

cursor.execute('''
CREATE TABLE stock (
    id INTEGER PRIMARY KEY,
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    symbol TEXT,
    adjclose REAL,
    dividends REAL,
    FOREIGN KEY(symbol) REFERENCES company(ticket)
)
''')

# --- STEP 3: Insert Data into DB ---
df_companies.to_sql('company', conn, if_exists='append', index=False)
df_prices.to_sql('stock', conn, if_exists='append', index=False)
conn.commit()

# --- STEP 4: Menu Functions ---

def list_companies():
    cursor.execute("SELECT ticket, company_name, sector FROM company ORDER BY ticket")
    rows = cursor.fetchall()
    print("\n📊 Company List:")
    for ticket, name, sector in rows:
        print(f"  {ticket} - {name} ({sector})")

def view_stock_operations():
    symbol = input("Enter ticket symbol (e.g., AAPL): ").upper()
    cursor.execute("SELECT * FROM stock WHERE symbol = ? ORDER BY date", (symbol,))
    rows = cursor.fetchall()
    print(f"\n📈 Stock operations for {symbol}:")
    for row in rows:
        print(row)

def filter_by_date():
    start = input("Start date (YYYY-MM-DD): ")
    end = input("End date (YYYY-MM-DD): ")
    print("Group by: (1) Day, (2) Week, (3) Month, (4) Year")
    granularity = input("Select grouping level (1–4): ")

    group_fields = {
        "1": ("strftime('%Y-%m-%d', date)", "Day"),
        "2": ("strftime('%Y-%W', date)", "Week"),
        "3": ("strftime('%Y-%m', date)", "Month"),
        "4": ("strftime('%Y', date)", "Year"),
    }

    if granularity not in group_fields:
        print("❌ Invalid choice. Defaulting to Day.")
        granularity = "1"


    group_by_expr, label = group_fields[granularity]

    query = f"""
            SELECT 
                symbol,
                {group_by_expr} AS group_label,
                AVG(open) AS avg_open,
                AVG(high) AS avg_high,
                AVG(low) AS avg_low,
                AVG(close) AS avg_close,
                SUM(volume) AS total_volume
            FROM stock
            WHERE date BETWEEN ? AND ?
            GROUP BY symbol, group_label
            ORDER BY symbol, group_label
        """

    try:
        cursor.execute(query, (start, end))
        rows = cursor.fetchall()

        print(f"\n📊 Stock Data ({label}-wise) from {start} to {end}:")
        print(f"{'Symbol':<10} {'Group':<12} {'Open':<10} {'High':<10} {'Low':<10} {'Close':<10} {'Volume':<12}")
        for row in rows:
            symbol, group_label, open_, high, low, close, volume = row
            print(
                f"{symbol:<10} {group_label:<12} {open_:<10.2f} {high:<10.2f} {low:<10.2f} {close:<10.2f} {volume:<12}")
    except Exception as e:
        print("❌ Error:", e)

""" 
def export_to_csv():
    symbol = input("Enter ticket symbol to export (or leave blank for all): ").upper()
    filename = input("Enter filename (e.g., report.csv): ")
    if symbol:
        query = "SELECT * FROM stock WHERE symbol = ? ORDER BY date"
        df = pd.read_sql_query(query, conn, params=(symbol,))
    else:
        df = pd.read_sql_query("SELECT * FROM stock ORDER BY symbol, date", conn)
    df.to_csv(filename, index=False)
    print(f"✅ Exported to {filename}")
"""



