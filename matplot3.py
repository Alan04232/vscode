import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

# Load the data
df = pd.read_csv("/home/alan/Desktop/workspace/space/ch3_libs/lib-v2/data/calibrated/20230825/ch3_lib_002_20230825T104221_00_l1/ch3_lib_002_20230825T104221_00_l1.csv", header=None)
print(df.head())
"""for col in df.columns:
    print(df[col], df[col].dtype)
    plt.plot(df[col], label=f'Column {col}')"""
plt.imshow(df[5:6], aspect='auto', cmap='viridis')
plt.colorbar(label='Value')
plt.legend()
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Line Plot of CSV Data')
plt.show()