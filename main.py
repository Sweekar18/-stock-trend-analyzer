import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def fetch_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def calculate_moving_averages(df, windows=[20, 50, 200]):
    for window in windows:
        df[f"MA_{window}"] = df['Close'].rolling(window=window).mean()
    return df

def identify_trends(df):
    latest = df.iloc[-1]
    print(latest[['MA_20', 'MA_50', 'MA_200']])  # Print values to check

    # Check for NaN before comparison
    if latest[['MA_20', 'MA_50', 'MA_200']].isnull().any():
        return "Insufficient data to identify trend (NaN values present)"
    
    # Use scalar values for comparison
    ma20 = latest['MA_20'].item() if hasattr(latest['MA_20'], 'item') else latest['MA_20']
    ma50 = latest['MA_50'].item() if hasattr(latest['MA_50'], 'item') else latest['MA_50']
    ma200 = latest['MA_200'].item() if hasattr(latest['MA_200'], 'item') else latest['MA_200']

    if ma20 > ma50 > ma200:
        return "Strong Bullish Trend"
    elif ma20 < ma50 < ma200:
        return "Strong Bearish Trend"
    else:
        return "Sideways/Unclear Trend"


def plot_stock(df, ticker):
    plt.figure(figsize=(14,7))
    plt.plot(df.index, df['Close'], label='Close Price')
    plt.plot(df.index, df['MA_20'], label='20-day MA')
    plt.plot(df.index, df['MA_50'], label='50-day MA')
    plt.plot(df.index, df['MA_200'], label='200-day MA')
    plt.title(f"{ticker} Stock Price and Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

def main():
    ticker = input("Enter stock ticker (e.g., AAPL, TSLA): ").upper()
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    data = fetch_stock_data(ticker, start_date, end_date)
    if data.empty:
        print("No data found for this ticker or date range.")
        return

    data = calculate_moving_averages(data)
    trend = identify_trends(data)

    print(f"Trend Analysis for {ticker}: {trend}")

    plot_stock(data, ticker)

if __name__ == "__main__":
    main()

