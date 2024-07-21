# Stock Volatility Forecasting App

This repository contains a Streamlit-based application for forecasting stock volatility using historical data and GARCH models. The application leverages data from Yahoo Finance to analyze the weekly volatility of selected stocks listed on the National Stock Exchange of India (NSE).

## Features

- **Stock Selection**: Choose from a list of major NSE stock tickers to analyze historical and forecasted volatility.
- **Historical Data Analysis**: Download and visualize historical stock data from 2005 to 2018.
- **Volatility Forecasting**: Utilize the GARCH (Generalized Autoregressive Conditional Heteroskedasticity) model to forecast weekly stock volatility in a rolling window manner.
- **Visualization**: Compare historical, forecasted, and actual volatility using interactive plots generated with Matplotlib.
- **Error Handling**: Graceful handling of missing data with warnings for unavailable ticker data.

## How to Run the App

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/stock-volatility-forecasting.git
   cd stock-volatility-forecasting
   ```

2. **Install Dependencies**:
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   Launch the Streamlit app with:
   ```bash
   streamlit run volatalitymodelling.py
   ```

4. **Use the App**:
   - Navigate to `http://localhost:8501` in your web browser.
   - Select a stock ticker from the dropdown menu to visualize and forecast its volatility.

## Dependencies

- `streamlit`: For creating the interactive web application.
- `yfinance`: To download historical stock data from Yahoo Finance.
- `pandas`: For data manipulation and analysis.
- `numpy`: For numerical computations.
- `arch`: To fit the GARCH model for volatility forecasting.
- `matplotlib`: For plotting historical and forecasted volatility.

## Code Explanation

- **Data Fetching**: Downloads historical and actual stock data for a specified date range using `yfinance`.
- **Volatility Calculation**: Calculates daily returns and weekly volatility for historical data.
- **Volatility Forecasting**: Implements a rolling forecast using a GARCH(1,1) model to predict future volatility.
- **Visualization**: Plots the historical, forecasted, and actual volatility for comparison.

## Handling KeyErrors

The code includes mechanisms to handle cases where data for a specific ticker might be unavailable, ensuring the app continues running smoothly by skipping those tickers and providing appropriate warnings.

## Future Improvements

- **Extend Ticker List**: Include more stocks from various exchanges.
- **Enhanced Forecasting**: Integrate additional models for improved accuracy.
- **User Customization**: Allow users to input custom date ranges and select multiple tickers.
