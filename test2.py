import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

# Correct file path (use raw string or double backslashes)
file_path = r"E:\vscode\Data\magic04.data"

# Column names
cols = ['fLength', 'fWidth', 'fSize', 'fConc', 'fConc1', 'fAsym',
        'fM3Long', 'fM3Trans', 'fAlpha', 'fDist', 'class']

# Load the dataset
df = pd.read_csv(file_path, names=cols)

# Plotting features
plt.figure(figsize=(12, 8))

plt.subplot(4, 1, 1)
plt.plot(df['fLength'], label='fLength', color='blue')
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(df['fWidth'], label='fWidth', color='green')
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(df['fSize'], label='fSize', color='orange')
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(df['fConc'], label='fConc', color='red')
plt.legend()

# Improve layout and display
plt.tight_layout()
plt.show()
