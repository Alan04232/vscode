#import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
colns=["flengths","fwidth","fsize","fconc","fconcl","fasym","fm3long","fm3trans","falpha","fdist","class"]
df=pd.read_csv("/home/alan/Desktop/workspace/space/magic+gamma+telescope/magic04.csv",names=colns)
print(df.head())
plt.plot(df.head("flength"))
plt.title("m")
plt.show()

