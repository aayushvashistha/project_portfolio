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

# Streamlit App Header
st.title('📈 Stock Trend Prediction')
st.markdown("""
**Disclaimer:**  
Predictions are based on historical stock data and machine learning models. Use them for educational purposes only.  
Consult a financial advisor before making investment decisions.
""")

# User Input
user_ip = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL)", 'AAPL')
start = "2010-01-01"
end = dt.date.today()

# Download data
df = yf.download(user_ip, start, end)

if df.empty:
    st.error("No data found for the given ticker. Please try a valid symbol.")
    st.stop()

# Display statistics
st.subheader('📊 Historical Data Summary')
st.write(df.describe())

# Visualization 1
st.subheader('📉 Closing Price vs Time')
fig = plt.figure(figsize=(12, 6))
plt.plot(df['Close'], label='Close Price')
plt.legend()
st.pyplot(fig)

# Moving Average 100
ma100 = df['Close'].rolling(100).mean()
st.subheader('📉 Close Price with 100-Day Moving Average')
fig = plt.figure(figsize=(12, 6))
plt.plot(df['Close'], label='Close Price')
plt.plot(ma100, 'r', label='100 MA')
plt.legend()
st.pyplot(fig)

# Moving Average 100 & 200
ma200 = df['Close'].rolling(200).mean()
st.subheader('📉 Close Price with 100 & 200-Day Moving Averages')
fig = plt.figure(figsize=(12, 6))
plt.plot(df['Close'], label='Close Price')
plt.plot(ma100, 'r', label='100 MA')
plt.plot(ma200, 'g', label='200 MA')
plt.legend()
st.pyplot(fig)

# Prepare training/testing datasets
data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):])

scaler = MinMaxScaler(feature_range=(0, 1))
data_training_array = scaler.fit_transform(data_training)

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'keras_model.h5')
if not os.path.exists(model_path):
    st.error("Trained model file not found. Please ensure 'keras_model.h5' exists.")
    st.stop()

model = load_model(model_path)

# Prepare test data
past_100_days = data_training.tail(100)
final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, len(input_data)):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i, 0])

x_test = np.array(x_test)
y_test = np.array(y_test)

# Predictions
y_predicted = model.predict(x_test)

# Rescale predictions
scale_factor = 1 / scaler.scale_[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

# Metrics
mae = mean_absolute_error(y_test, y_predicted)
rmse = np.sqrt(mean_squared_error(y_test, y_predicted))
r2 = r2_score(y_test, y_predicted)

# Display metrics
st.subheader("📈 Model Performance Metrics")
st.write(f"**Mean Absolute Error (MAE):** {mae:.2f}")
st.write(f"**Root Mean Squared Error (RMSE):** {rmse:.2f}")
st.write(f"**R-squared Score (R²):** {r2:.2f}")

# Feedback based on R²
if r2 > 0.9:
    st.success("The model shows strong predictive performance.")
else:
    st.warning("The model predictions have some error. Interpret with caution.")

# Plot predictions
st.subheader('🔮 Predicted vs Actual Closing Prices')
fig2 = plt.figure(figsize=(12, 6))
plt.plot(y_test, label='Actual Price')
plt.plot(y_predicted, label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()
st.pyplot(fig2)

# Predict next day
next_day_input = input_data[-100:].reshape(1, 100, 1)
next_day_prediction = model.predict(next_day_input)
next_day_prediction = next_day_prediction * scale_factor

predicted_price = f"${next_day_prediction[0][0]:.2f}"
st.markdown(f"### 📌 **Predicted Next Day Price: {predicted_price}**")

print("------ STREAMLIT APP ENDED SUCCESSFULLY ------")