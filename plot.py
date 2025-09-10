import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
colns=["flengths","fwidth","fsize","fconc","fconcl","fasym","fm3long","fm3trans","falpha","fdist","class"]
df=pd.read_csv("/home/alan/Desktop/workspace/space/magic+gamma+telescope/magic04.csv",names=colns)
print(df.head())
plt.subplot(2, 1, 1)
plt.plot(df["flengths"],df["fsize"],'ro')
plt.xlabel("s")
plt.ylabel("size")
plt.plot(df["flengths"],df["fwidth"],'ro')
plt.xlabel("s")
plt.ylabel("w")
plt.title("m")
plt.tight_layout()
plt.show()

