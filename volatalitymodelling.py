import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from arch import arch_model
import matplotlib.pyplot as plt

# Define the list of stock tickers
tickers = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS",
    "SBIN.NS", "INFY.NS", "HINDUNILVR.NS", "ITC.NS", "LT.NS",
    "HCLTECH.NS", "BAJFINANCE.NS", "ONGC.NS", "AXISBANK.NS", 
    "MARUTI.NS", "SUNPHARMA.NS", "TATAMOTORS.NS", "KOTAKBANK.NS", "NTPC.NS"
]

# Define the historical date range
start_date = "2005-01-01"
end_date = "2018-07-31"

# Define the forecast period
forecast_start_date = "2018-09-01"
forecast_end_date = "2024-02-29"

# Download historical data
data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')

# Extract the 'Adj Close' prices
adj_close_data = {ticker: data[ticker]['Adj Close'] for ticker in tickers}

# Convert to DataFrame
df = pd.DataFrame(adj_close_data)

# Calculate daily returns
daily_returns = df.pct_change()

# Resample to weekly returns and calculate weekly volatility
weekly_volatility = daily_returns.resample('W').std()

# Download actual data for the forecast period
actual_data = yf.download(tickers, start=forecast_start_date, end=forecast_end_date, group_by='ticker')

# Extract the 'Adj Close' prices for the actual data
actual_adj_close_data = {ticker: actual_data[ticker]['Adj Close'] for ticker in tickers}

# Convert to DataFrame
actual_df = pd.DataFrame(actual_adj_close_data)

# Calculate actual daily returns and weekly volatility for the forecast period
actual_daily_returns = actual_df.pct_change()
actual_weekly_volatility = actual_daily_returns.resample('W').std()

# Combine historical and actual data
combined_volatility = pd.concat([weekly_volatility, actual_weekly_volatility])

# Function to forecast volatility using GARCH in a rolling window manner
def rolling_forecast_volatility(volatility_series, forecast_start, forecast_end):
    forecast_dates = pd.date_range(start=forecast_start, end=forecast_end, freq='W')
    forecasts = []
    
    # Ensure the index of the volatility series is timezone-aware
    if volatility_series.index.tz is None:
        volatility_series.index = volatility_series.index.tz_localize('UTC')

    for date in forecast_dates:
        # Ensure the forecast date is timezone-aware
        if date.tz is None:
            date = date.tz_localize('UTC')
        
        # Select data up to the current date
        current_data = volatility_series.loc[:date].dropna()
        
        if len(current_data) < 1:
            forecasts.append(np.nan)
            continue
        
        # Rescale the data
        rescaled_data = 100 * current_data
        
        # Fit GARCH model
        garch_model = arch_model(rescaled_data, vol='Garch', p=1, q=1)
        model_fit = garch_model.fit(disp='off')
        
        # Forecast the next week's volatility
        forecast = model_fit.forecast(horizon=1)
        forecast_volatility = np.sqrt(forecast.variance.values[-1, 0]) / 100  # Rescale back
        
        forecasts.append(forecast_volatility)
    
    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Forecasted Volatility': forecasts})
    
    return forecast_df

# Streamlit App
st.title('Stock Volatility Forecasting')

# Dropdown menu for selecting a stock
selected_ticker = st.selectbox('Select a stock:', tickers)

if selected_ticker:
    st.write(f"Forecasting volatility for {selected_ticker}...")

    # Forecast volatility
    volatility_series = combined_volatility[selected_ticker]
    forecasted_volatility = rolling_forecast_volatility(volatility_series, forecast_start_date, forecast_end_date)
    
    # Plot the results
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(volatility_series.index, volatility_series, label='Historical Volatility', color='blue')
    ax.plot(forecasted_volatility['Date'], forecasted_volatility['Forecasted Volatility'], label='Forecasted Volatility', color='red')
    
    # If actual volatility series exists, plot it
    if selected_ticker in actual_weekly_volatility:
        ax.plot(actual_weekly_volatility.index, actual_weekly_volatility[selected_ticker], 
                label='Actual Volatility', color='gray', linestyle='--')
    
    ax.set_title(f'Weekly Volatility Forecast for {selected_ticker}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Volatility')
    ax.legend(loc='upper left')

    # Display the plot
    st.pyplot(fig)
