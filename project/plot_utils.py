import matplotlib.pyplot as plt


def plot_stock_data(df, ticker, column, label):
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df[column], label=label, color="blue")
    plt.title(f"{ticker} {label}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.show()
