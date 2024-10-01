import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Get user inputs
ticker_input = input("Enter the stock ticker (e.g., AAPL, TSLA): ").upper()
period_input = input("Enter the time period (e.g., '1mo', '3mo', '1y'): ")
file_name = input("Enter the name of the Excel file to save the data (e.g., 'stock_data.xlsx'): ")

try:
    
    stock = yf.Ticker(ticker_input)
    hist = stock.history(period=period_input)
    
    if hist.empty:
        raise ValueError("No data available for the given input.")

   
    hist['5-Day MA'] = hist['Close'].rolling(window=5).mean()

    
    print(hist[['Close', '5-Day MA']])

    
    plot_input = input("Do you want to plot the stock price and 5-day moving average? (yes/no): ").lower()

    if plot_input == "yes":
       
        plt.figure(figsize=(10, 5))
        plt.plot(hist.index, hist['Close'], label="Closing Price", color="blue")
        plt.title(f"{ticker_input} Stock Price")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid()
        plt.show()

       
        plt.figure(figsize=(10, 5))
        plt.plot(hist.index, hist['5-Day MA'], label="5-Day Moving Average", color="orange")
        plt.title(f"{ticker_input} 5-Day Moving Average")
        plt.xlabel("Date")
        plt.ylabel("Moving Average")
        plt.legend()
        plt.grid()
        plt.show()

    
    hist.index = hist.index.tz_localize(None)

    
    hist.to_excel(file_name)
    print(f"Stock data with 5-Day Moving Average has been exported to {file_name}")

    
    df = pd.read_excel(file_name)
    print(df)

except Exception as e:
    print(f"An error occurred: {e}")
