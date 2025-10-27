import numpy as np
# Input signal and filter
xn = np.array([3, -1, 0, 1, 3, 2, 0, 1, 2, 1])
hn = np.array([1, 1, 1])
M = len(hn)          # filter length
L = 4                # block length (new samples per block)
N = L + M - 1        # total block length including overlap
# Pad filter to length N
h = np.pad(hn, (0, N - M), 'constant')
print(f"Filter padded: {h}")
y = [] 
# Overlap-save 
for i in range(0, len(xn), L):
    if i == 0:
        x = np.pad(xn[i:i+L], (M-1, 0), 'constant')
    else:
        x = np.concatenate((xn[i-(M-1):i], xn[i:i+L]))
    if len(x) < N:
        x = np.pad(x, (0, N - len(x)), 'constant')   #pad the x
    print(f"\nBlock {i//L + 1}: {x}")
    y_block = np.convolve(x, h, mode='full') # convolution process
    y_valid = y_block[M-1:M-1+L]
    y.extend(y_valid)
y =np.array(y)
print("\nFinal Overlap-Save Output:", y)