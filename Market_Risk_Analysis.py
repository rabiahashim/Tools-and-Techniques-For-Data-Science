# Import necessary libraries
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
    end_date = st.date_input("Enter end date:")

    # Fetch stock data
    stocks_data = get_stock_data(symbols, start_date, end_date)

    # Display stock data
    st.header("Stock Data")
    #st.write(stocks_data.head())
    st.dataframe(stocks_data.head())

    # Calculate beta and make investment decisions
    st.header("Investment Decisions")

    # Check if symbols are provided and contain at least one non-empty symbol
    if symbols and any(symbol.strip() for symbol in symbols):
        for symbol in symbols:
            # Skip empty or whitespace-only symbols
            if not symbol.strip():
                continue

            # Check if the symbol is present in the stocks_data DataFrame
            if symbol in stocks_data.columns:
                stock_returns = stocks_data[symbol].pct_change().dropna()
                market_returns = yf.download('^GSPC', start=start_date, end=end_date)['Adj Close'].pct_change().dropna()

                # Merge and align DataFrames based on date index
                df = pd.merge(stock_returns, market_returns, how='inner', left_index=True, right_index=True)
                # st.write(df.head())

                stock_symbols = symbol
                stock_returns_up = df[stock_symbols]
                market_returns_up = df['Adj Close']
                # st.write(stock_returns_up)

                beta = calculate_beta(stock_returns_up, market_returns_up)
                decision = make_investment_decision(beta)

                st.write(f"For {symbol}, Beta: {beta:.4f}")
                st.write(f"Investment Decision: {decision}")
            else:
                st.warning(f"Stock symbol '{symbol}' not found in the dataset.")
    else:
        st.write("Please enter valid stock indices to view betas")

if __name__ == "__main__":
    main()
