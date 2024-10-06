import yfinance as yf
import pandas as pd

# Ticker mapping for renamed companies or common issues with tickers
TICKER_MAPPING = {
    "FB": "META",  # Facebook changed its ticker to META
    # You can add more mappings here as needed
}


def fetch_stock_history(ticker: str, period: str) -> pd.DataFrame:
    # Check for ticker mapping
    ticker = TICKER_MAPPING.get(ticker, ticker)  # Replace ticker if mapped

    # Fetch stock history from yfinance
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)

    if hist.empty:
        raise ValueError(f"No data available for the stock ticker: {ticker}. It might be delisted or unavailable.")
    
    return hist

def filter_stocks_by_price(tickers: list, period: str, lower_bound: float, upper_bound: float) -> pd.DataFrame:
    filtered_data_list = []

    for ticker in tickers:
        try:
            hist = fetch_stock_history(ticker, period)
            hist['Ticker'] = ticker
            
            # Debug: Print the last closing price for the ticker
            print(f"{ticker} last close price: {hist['Close'].iloc[-1]}")

            filtered_data = hist[(hist['Close'] >= lower_bound) & (hist['Close'] <= upper_bound)]
            if not filtered_data.empty:
                filtered_data_list.append(filtered_data)
        except ValueError as e:
            print(f"Error fetching data for {ticker}: {e}")

    if filtered_data_list:
        return pd.concat(filtered_data_list, axis=0)
    
    return pd.DataFrame()
