import numpy as np
x=np.random.random(8)
h=np.random.random(8)
N=len(x)
z=(x+h*1j)
print(z)
def sum_td(z,N):
    
    sum=0
    for i in range(N):
        sum=sum+z[i]
    return sum
def sum_fd(z,N):
    num=np.arange(N)
    for k in range (N):
        xk=0
        for n in range(N):
            xk=np.exp(((-2j)*(np.pi*n)/N)*(n*k))    
            num[n]+=xk*z[n]   
            #deactivate

    return num
sum2=0
num=sum_fd(z,N)
for i in range(N):
    sum2+=num[i]
sum=np.sum(abs(sum_td(z,N)))
sum2=np.sum(sum_fd(z,N))
print(sum)
print(sum2)                    