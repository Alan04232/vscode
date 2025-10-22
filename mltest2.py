import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# ===============================
# Load MAGIC dataset
# ===============================
cols = ['fLength', 'fWidth', 'fSize', 'fConc', 'fConc1', 'fAsym',
        'fM3Long', 'fM3Trans', 'fAlpha', 'fDist', 'class']

df = pd.read_csv("/mnt/d/workspace/data/magic+gamma+telescope/magic04.data", names=cols)

# Choose one feature column for sequence prediction
series = df["fLength"].values.astype(float)

# ===============================
# Preprocess: scale data
# ===============================
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(series.reshape(-1, 1))

# Function to create sequences
def create_dataset(series, look_back=20):
    X, y = [], []
    for i in range(len(series) - look_back):
        X.append(series[i:i+look_back])
        y.append(series[i+look_back])
    return np.array(X), np.array(y)

look_back = 20
X, y = create_dataset(data_scaled, look_back)

# Reshape to [samples, timesteps, features]
X = X.reshape(X.shape[0], X.shape[1], 1)

# Train/Test split
split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# ===============================
# Build LSTM model
# ===============================
model = Sequential([
    LSTM(64, input_shape=(look_back, 1)),
    Dense(1)
])
model.compile(optimizer="adam", loss="mse")
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test), verbose=1)

# ===============================
# Predict on test set
# ===============================
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)
y_test_inv = scaler.inverse_transform(y_test)

plt.figure(figsize=(10,5))
plt.plot(y_test_inv, label="True")
plt.plot(predictions, label="Predicted")
plt.legend()
plt.title("Test Predictions on fLength")
plt.show()

# ===============================
# Predict next 100 future values
# ===============================
future_steps = 100
last_seq = data_scaled[-look_back:]
future_preds = []

current_seq = last_seq.reshape(1, look_back, 1)
for _ in range(future_steps):
    next_val = model.predict(current_seq)[0]
    future_preds.append(next_val)
    current_seq = np.append(current_seq[:, 1:, :], [[next_val]], axis=1)

future_preds = scaler.inverse_transform(np.array(future_preds).reshape(-1, 1))

plt.figure(figsize=(10,5))
plt.plot(range(len(series)), series, label="Original Data")
plt.plot(range(len(series), len(series)+future_steps), future_preds, label="Future Predictions", color="red")
plt.legend()
plt.title("Next 100 Value Predictions (fLength)")
plt.show()
