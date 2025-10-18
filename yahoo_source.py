
import pandas as pd
from yahooquery import Ticker

# Define the stock tickers
tickers = ['MSFT', 'IBM', 'AAPL']

# Fetch data using yahooquery
stocks = Ticker(tickers)

# --- Get Summary Profile Info (Company Information) ---
def get_company_info(ticker):
    summary = stocks.summary_profile[ticker]
    return {
        'Ticker': ticker,
        'Name': stocks.quotes[ticker]['shortName'],
        'Sector': summary.get('sector', 'N/A'),
        'Industry': summary.get('industry', 'N/A'),
        'CEO': summary.get('companyOfficers', [{}])[0].get('name', 'N/A') if summary.get('companyOfficers') else 'N/A',
        'Employees': summary.get('fullTimeEmployees', 'N/A'),
        'Website': summary.get('website', 'N/A'),
    }

# Compile company info for all tickers
company_info = pd.DataFrame([get_company_info(tk) for tk in tickers])
print("=== Company Information ===")
print(company_info)

# --- Get Historical Price Data ---
# Example: Last 30 days of daily price data
price_history = stocks.history(period="1mo", interval="1d")

# Reset index for easier manipulation (multi-index)
price_history = price_history.reset_index()
print("\n=== Price History (Last 30 Days) ===")
print(price_history.head())

# Optional: Save results to CSV
company_info.to_csv('company_info.csv', index=False)
price_history.to_csv('stock_price_history.csv', index=False)
