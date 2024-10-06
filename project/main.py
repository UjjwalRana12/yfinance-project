from models import StockQuery
from stocks_utils import fetch_stock_history, filter_stocks_by_price
from plot_utils import plot_stock_data
from export_utils import export_to_excel

def process_by_ticker():
    try:
        stock_query = StockQuery(
            ticker=input("Enter the stock ticker (e.g., AAPL, TSLA): ").upper(),
            period=input("Enter the time period (e.g., '1mo', '3mo', '1y'): "),
            file_name=input("Enter the name of the Excel file to save the data (e.g., 'stock_data.xlsx'): ")
        )

        hist = fetch_stock_history(stock_query.ticker, stock_query.period)
        hist['5-Day MA'] = hist['Close'].rolling(window=5).mean()

        print(hist[['Close', '5-Day MA']])

        if input("Do you want to plot the stock price and 5-day moving average? (yes/no): ").lower() == "yes":
            plot_stock_data(hist, stock_query.ticker, 'Close', 'Closing Price')
            plot_stock_data(hist, stock_query.ticker, '5-Day MA', '5-Day Moving Average')

        export_to_excel(hist, stock_query.file_name)

    except Exception as e:
        print(f"An error occurred: {e}")

def process_by_price():
    try:
        stock_query = StockQuery(
            period=input("Enter the time period (e.g., '1mo', '3mo', '1y'): "),
            file_name=input("Enter the name of the Excel file to save the data (e.g., 'stock_data.xlsx'): "),
            close_price=float(input("Enter the closing price to filter stocks: "))
        )

        lower_bound = stock_query.close_price - 100
        upper_bound = stock_query.close_price + 100

        tickers = [
    "AAPL", "TSLA", "GOOGL", "MSFT", "AMZN", "NFLX", "FB", "NVDA", "BABA", "V",     
    "JPM", "UNH", "HD", "PG", "MA", "DIS", "PYPL", "ADBE", "INTC", "CSCO",           
    "CRM", "PFE", "MRK", "KO", "PEP", "NKE", "COST", "XOM", "WMT", "T",              
    "BA", "MMM", "IBM", "ORCL", "CAT", "CVX", "RTX", "QCOM", "AVGO", "SBUX",         
    "MDT", "SPGI", "TMO", "BLK", "AMAT", "GE", "AMGN", "GILD", "HON", "TXN",         
    "LMT", "LLY", "SCHW", "NOW", "DHR", "ZTS", "C", "ISRG", "BKNG", "GS",            
    "SCHD", "UNP", "MS", "AXP", "MCD", "ABBV", "LOW", "UPS", "ADI", "FISV"          
]

        filtered_data = filter_stocks_by_price(tickers, stock_query.period, lower_bound, upper_bound)

        if not filtered_data.empty:
            print(f"Stocks with closing prices in the range {lower_bound} - {upper_bound}:")
            print(filtered_data[['Ticker', 'Close']])

            if input("Do you want to plot the stock prices for the filtered data? (yes/no): ").lower() == "yes":
                for ticker in filtered_data['Ticker'].unique():
                    stock_data = filtered_data[filtered_data['Ticker'] == ticker]
                    plot_stock_data(stock_data, ticker, 'Close', 'Closing Price')

            export_to_excel(filtered_data, stock_query.file_name)
        else:
            print(f"No stocks found with closing prices in the range {lower_bound} - {upper_bound}.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    search_choice = input("Do you want to search by stock ticker or close price? (Enter 'ticker' or 'price'): ").lower()

    if search_choice == "ticker":
        process_by_ticker()
    elif search_choice == "price":
        process_by_price()
    else:
        print("Invalid choice. Please enter 'ticker' or 'price'.")
