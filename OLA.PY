import numpy as np

xn = np.array([3, -1, 0, 1, 3, 2, 0, 1, 2, 1])
hn = np.array([1, 1, 1])

                 # block size
M = L= len(hn)
N = L + M - 1           # length of each block convolution

x=[]
# Split into segments
for i in range(0, len(xn), L):
    a = xn[i:i+L]
    x.append(a)
print("x_split =", x)

# Initialize final output
y = np.zeros(len(xn) + len(hn) - 1)

# Manual index-based loop
for k in range(len(x)):
    i = x[k]  # get block at index k

    # Pad last block if necessary
    if len(i) < L:
        i = np.pad(i, (0, L - len(i)))
    print(i)
    # Convolve this block with h[n]
    yn = np.convolve(i, hn)

    # Overlap-add: add to correct position
    z = k * L
    d = z + len(yn)
    if d > len(y):
        y[z:] += yn[:len(y) - z]
    else:
        y[z:d] += yn

print("Final y[n] =", y)
