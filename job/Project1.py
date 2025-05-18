import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt
from keras.models import load_model
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os

# Streamlit Application Header
st.title('Stock Trend Prediction')
st.markdown("""
**Disclaimer:** 
The predictions made by this model are based on historical data and machine learning algorithms. They should not be used as a sole basis for any investment decision. The stock market is unpredictable, and future prices may differ from the predictions shown here. Please consult a financial advisor before making investment decisions.
""")

# User Input for Stock Ticker
user_ip = st.text_input("Enter stock Ticker", 'AAPL')
start = "2010-01-01"
end = dt.date.today()

# Download data using yfinance
df = yf.download(user_ip, start, end)

# Display statistical summary of data
st.subheader('Data from 2010 - till date')
st.write(df.describe())

# Visualizations
st.subheader('Closing Price vs Time Chart')
fig = plt.figure(figsize=(12, 6))
plt.plot(df.Close)
st.pyplot(fig)

# 100 Moving Average Visualization
st.subheader('Closing Price vs Time Chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(df.Close)
plt.plot(ma100, 'r', label='100 Day Moving Average')
plt.legend()
st.pyplot(fig)

# 100 and 200 Moving Averages Visualization
st.subheader('Closing Price vs Time Chart with 100MA & 200MA')
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(ma100, 'r', label='100 Day Moving Average')
plt.plot(ma200, 'g', label='200 Day Moving Average')
plt.plot(df.Close, 'b', label='Actual Closing Price')
plt.legend()
st.pyplot(fig)

# Splitting data into Training and Testing
data_training = pd.DataFrame(df['Close'][0:int(len(df) * 0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df) * 0.70): int(len(df))])

# Scaling the data
scaler = MinMaxScaler(feature_range=(0, 1))
data_training_array = scaler.fit_transform(data_training)

# Load the pre-trained model
model = load_model(os.path.join(os.path.dirname(__file__), 'keras_model.h5'))

# Preparing data for prediction
past_100_days = data_training.tail(100)
final_df = past_100_days.append(data_testing, ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

# Creating test datasets
for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100: i])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)

# Making Predictions
y_predicted = model.predict(x_test)

# Inversing scaling to get the actual predicted prices
scaler = scaler.scale_
scale_factor = 1 / scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

# Performance Metrics
mae = mean_absolute_error(y_test, y_predicted)
rmse = np.sqrt(mean_squared_error(y_test, y_predicted))
r2 = r2_score(y_test, y_predicted)

# Display performance metrics
st.subheader("**Model Performance Metrics**")
st.write(f"Mean Absolute Error (MAE): {mae:.4f}")
st.write(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
st.write(f"R-squared: {r2:.4f}")

# Display a suggestion based on the model's performance
if r2 > 0.9:
    st.write("The model's predictions are quite accurate, but still, do not rely solely on them for investment decisions. Past performance does not guarantee future results.")
else:
    st.write("The model's predictions show some discrepancy with the actual data. Please be cautious and consult a financial advisor.")

# Final Visualization of Predictions vs Original Data
st.subheader('Predictions vs Original')
fig2 = plt.figure(figsize=(12, 6))
plt.plot(y_test, 'b', label='Original Price')
plt.plot(y_predicted, 'g', label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)

# Display predicted stock price for the next day
next_day_prediction = model.predict(input_data[-100:].reshape(1, 100, 1))
next_day_prediction = next_day_prediction * scale_factor  # Scale back to original
predicted_price = f"${next_day_prediction[0][0]:.2f}"

st.markdown(f"### 🚀 **Predicted stock price for the next day: {predicted_price}**")

print("------EXITING STREAMLIT PROJECT 1-----------------")
