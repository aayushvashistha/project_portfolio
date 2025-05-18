import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import datetime as dt

# Download stock data
ticker = 'AAPL'
start = "2010-01-01"
end = dt.date.today()
df = yf.download(ticker, start, end)

# Prepare data
data = df[['Close']]
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

train_size = int(len(data_scaled) * 0.70)
train_data = data_scaled[:train_size]

x_train, y_train = [], []
for i in range(100, len(train_data)):
    x_train.append(train_data[i-100:i])
    y_train.append(train_data[i])

x_train, y_train = np.array(x_train), np.array(y_train)

# Build model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(100, 1)))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train
model.fit(x_train, y_train, epochs=10, batch_size=32)

# Save
model.save('./job/keras_model.h5')
