from pydantic import BaseModel, Field
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd


class StockQuery(BaseModel):
    ticker: str = Field(None, description="The stock ticker symbol", example="AAPL")
    period: str = Field(..., description="The period for fetching stock data (e.g., '1mo', '3mo', '1y')", example="1mo")
    file_name: str = Field(..., description="The Excel file name to save the data", example="stock_data.xlsx")
    close_price: float = Field(None, description="The closing price to filter stocks", example=3000.0)

try:
    
    search_choice = input("Do you want to search by stock ticker or close price? (Enter 'ticker' or 'price'): ").lower()

    if search_choice == "ticker":
        stock_query = StockQuery(
            ticker=input("Enter the stock ticker (e.g., AAPL, TSLA): ").upper(),
            period=input("Enter the time period (e.g., '1mo', '3mo', '1y'): "),
            file_name=input("Enter the name of the Excel file to save the data (e.g., 'stock_data.xlsx'): ")
        )
        
        
        stock = yf.Ticker(stock_query.ticker)
        hist = stock.history(period=stock_query.period)
        
        if hist.empty:
            raise ValueError("No data available for the given stock ticker.")

        
        hist['5-Day MA'] = hist['Close'].rolling(window=5).mean()
        print(hist[['Close', '5-Day MA']])

       
        plot_input = input("Do you want to plot the stock price and 5-day moving average? (yes/no): ").lower()

        if plot_input == "yes":
            
            plt.figure(figsize=(10, 5))
            plt.plot(hist.index, hist['Close'], label="Closing Price", color="blue")
            plt.title(f"{stock_query.ticker} Stock Price")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.legend()
            plt.grid()
            plt.show()

            
            plt.figure(figsize=(10, 5))
            plt.plot(hist.index, hist['5-Day MA'], label="5-Day Moving Average", color="orange")
            plt.title(f"{stock_query.ticker} 5-Day Moving Average")
            plt.xlabel("Date")
            plt.ylabel("Moving Average")
            plt.legend()
            plt.grid()
            plt.show()

        
        hist.index = hist.index.tz_localize(None)
        hist.to_excel(stock_query.file_name)
        print(f"Stock data with 5-Day Moving Average has been exported to {stock_query.file_name}")

    elif search_choice == "price":
        
        stock_query = StockQuery(
            period=input("Enter the time period (e.g., '1mo', '3mo', '1y'): "),
            file_name=input("Enter the name of the Excel file to save the data (e.g., 'stock_data.xlsx'): "),
            close_price=float(input("Enter the closing price to filter stocks: "))
        )

        
        lower_bound = stock_query.close_price - 100
        upper_bound = stock_query.close_price + 100

        
        tickers = ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN", "NFLX", "FB", "NVDA", "BABA", "V"]
        filtered_data_list = []

        for ticker in tickers:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=stock_query.period)
            if not hist.empty:
                hist['Ticker'] = ticker
                
                filtered_data = hist[(hist['Close'] >= lower_bound) & (hist['Close'] <= upper_bound)]
                if not filtered_data.empty:
                    filtered_data_list.append(filtered_data)

        
        if len(filtered_data_list) > 0:
            # Concatenate the filtered data into a single DataFrame
            filtered_data = pd.concat(filtered_data_list, axis=0)
            print(f"Stocks with closing prices in the range {lower_bound} - {upper_bound}:")
            print(filtered_data[['Ticker', 'Close']])

            
            plot_input = input("Do you want to plot the stock price for the filtered data? (yes/no): ").lower()

            if plot_input == "yes":
                
                for ticker in filtered_data['Ticker'].unique():
                    stock_data = filtered_data[filtered_data['Ticker'] == ticker]
                    plt.figure(figsize=(10, 5))
                    plt.plot(stock_data.index, stock_data['Close'], label=f"{ticker} Closing Price", color="blue")
                    plt.title(f"{ticker} Stock Price")
                    plt.xlabel("Date")
                    plt.ylabel("Price")
                    plt.legend()
                    plt.grid()
                    plt.show()

           
            filtered_data.index = filtered_data.index.tz_localize(None)
            filtered_data.to_excel(stock_query.file_name)
            print(f"Filtered stock data has been exported to {stock_query.file_name}")
        else:
            print(f"No stocks found with closing prices in the range {lower_bound} - {upper_bound}.")

    else:
        print("Invalid choice. Please enter 'ticker' or 'price'.")

except Exception as e:
    print(f"An error occurred: {e}")
