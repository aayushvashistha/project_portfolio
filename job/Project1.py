import yfinance as yf
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np
# import pandas_datareader as data
from sklearn.preprocessing import MinMaxScaler
import datetime as dt
from keras.models import load_model
import streamlit as st
import os

print("---------------inside streamli project 1 ------------------")
start = "2010-01-01"
end = dt.date.today()

st.title('Stock Trend Prediction')

user_ip = st.text_input("Enter stock Ticker", 'AAPL')
df = yf.download(user_ip, start, end)

st.subheader('Data from 2010 - till date')
st.write(df.describe())

#Visualizations:
st.subheader('Closing Price vs Time Chart')
fig = plt.figure(figsize= (12,6))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time Chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize= (12,6))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time Chart with 100MA & 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize= (12,6))
plt.plot(ma100, 'r')
plt.plot(ma200, 'g')
plt.plot(df.Close, 'b')
st.pyplot(fig)

# Splitting data into Training and Testing

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])

scaler = MinMaxScaler(feature_range=(0,1))

data_training_array = scaler.fit_transform(data_training)

model = load_model(os.path.join(os.path.dirname(__file__), 'keras_model.h5'))

past_100_days = data_training.tail(100)
final_df = past_100_days.append(data_testing, ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100: i])
    y_test.append(input_data[i, 0])


x_test, y_test = np.array(x_test), np.array(y_test)
y_predicted = model.predict(x_test)
scaler = scaler.scale_

scale_factor = 1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

# Final Visualization

st.subheader('Predictions vs Original')
fig2 = plt.figure(figsize=(12, 6))
plt.plot(y_test, 'b', label= 'Original Price')
plt.plot(y_predicted, 'g', label= 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)

print("------EXITING STREAMLIT PROJECT 1-----------------")