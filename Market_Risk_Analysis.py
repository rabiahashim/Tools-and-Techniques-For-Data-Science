import streamlit as st
from pandas_datareader import wb
from datetime import datetime
import yfinance as yf
import numpy as np
import pandas as pd

# Function to fetch stock data
def get_stock_data(symbols, start_date, end_date):
    stock_data = yf.download(symbols, start=start_date, end=end_date)['Adj Close']
    return stock_data

# Function to calculate beta
def calculate_beta(stock_returns, market_returns):
    covariance_matrix = np.cov(stock_returns, market_returns)
    beta = covariance_matrix[0, 1] / np.var(market_returns)
    return beta

# Function to make investment decision based on beta
def make_investment_decision(beta):
    if beta > 1.2:
        return "Highly Volatile: Consider the high risk and potential high returns. Monitor closely."
    elif 0.8 <= beta <= 1.2:
        return "Moderate Volatility: Generally in line with the market. Assess other factors for decision-making."
    else:
        return "Low Volatility: Relatively stable. Suitable for conservative investors."

# Streamlit app
def main():
    st.title("Market Risk Analysis and Stock Forecasting App")

    # User input for stock symbols
    symbols = st.text_input("Enter multiple stock symbols separated by commas (e.g., AAPL,GOOGL,MSFT):").split(',')

    # User input for date range
    start_date = st.date_input("Enter start date:")
    end_date = st.date_input("Enter end date:", value=datetime.today())

    if st.button('Fetch Data'):
        if start_date > end_date:
            st.error("Start date must be before end date.")
        elif not symbols or all(symbol.strip() == '' for symbol in symbols):
            st.error("Please enter at least one valid stock symbol.")
        else:
            # Fetch stock data
            stocks_data = get_stock_data(symbols, start_date, end_date)

            # Display stock data
            st.header("Stock Data")
            st.dataframe(stocks_data.head())

            # Calculate beta and make investment decisions
            st.header("Investment Decisions")
            print(stocks_data.columns)
            for symbol in symbols:
                symbol = symbol.strip()
                if symbol and symbol in stocks_data.columns:
                    stock_returns = stocks_data[symbol].pct_change().dropna()
                    market_returns = yf.download('^GSPC', start=start_date, end=end_date)['Adj Close'].pct_change().dropna()

                    # Merge and align DataFrames based on date index
                    df = pd.merge(stock_returns, market_returns, how='inner', left_index=True, right_index=True)
                    stock_returns_aligned = df.iloc[:, 0]
                    market_returns_aligned = df.iloc[:, 1]

                    beta = calculate_beta(stock_returns_aligned, market_returns_aligned)
                    decision = make_investment_decision(beta)

                    st.write(f"For {symbol}, Beta: {beta:.4f}")
                    st.write(f"Investment Decision: {decision}")
                else:
                    st.warning(f"Stock symbol '{symbol}' not found in the dataset.")

if __name__ == "__main__":
    main()
