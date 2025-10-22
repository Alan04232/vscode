import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

# Correct file path (use raw string or double backslashes)


# Column names
cols = ['fLength', 'fWidth', 'fSize', 'fConc', 'fConc1', 'fAsym',
        'fM3Long', 'fM3Trans', 'fAlpha', 'fDist', 'class']

# Load the dataset
df = pd.read_csv("D:\workspace\data\magic+gamma+telescope\magic04.data", names=cols)
df["class"]= (df['class'] == 'g').astype(int)  # Convert 'g' to 1 and 'h' to 0
print(df.head())
"""for label in cols[:-1]:
    plt.hist(df[df["class"]==1][label],color='blue',label='gamma',alpha=0.5,density=True)
    plt.hist(df[df["class"]==0][label],color='green',label='hardon',alpha=0.5,density=True)
    
    plt.title(label)
    plt.xlabel(label)
    plt.ylabel('probability density')
    plt.legend()
    plt.tight_layout()
    plt.show()

"""

train,vaild,test =np.split(df.sample(frac=1),[int(0.6*len(df)),int(0.8*len(df))])
def scale_dataset(dataframe ,oversample=False):
    x=dataframe[dataframe.columns[:-1]].values
    y=dataframe[dataframe.columns[-1]].values
    scaler =StandardScaler()
    x= scaler.fit_transform(x)
    if oversample:
        ros = RandomOverSampler()
        x,y = ros.fit_resample(x ,y)
    data =np.hstack((x,np.reshape(y,(-1,1))))
    
    return data , x,y
train  , x_train ,y_train =scale_dataset(train,oversample=True)
vaild , x_train ,y_train =scale_dataset(vaild,oversample=False)
test , x_train ,y_train =scale_dataset(test,oversample=False)


knn_model = KNeighborsClassifier(n_neighbors=1)
knn_model.fit(x_train, y_train)
y_pred = knn_model.predict(x_train)
print(classification_report(y_train, y_pred))
