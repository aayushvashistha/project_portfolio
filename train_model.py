import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense
import datetime as dt
import os

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

# Build model using Input layer explicitly
input_layer = Input(shape=(100, 1), name="input_layer")
x = LSTM(50, return_sequences=True)(input_layer)
x = LSTM(50)(x)
output = Dense(1)(x)

model = Model(inputs=input_layer, outputs=output)
model.compile(optimizer='adam', loss='mean_squared_error')

# Train model
model.fit(x_train, y_train, epochs=10, batch_size=32)

# Create output directory if it doesn't exist
output_dir = './job'
os.makedirs(output_dir, exist_ok=True)

# Save model safely (HDF5 format, now compatible for loading)
model.save(os.path.join(output_dir, 'keras_model.keras'))

print("✅ Model training and saving complete.")