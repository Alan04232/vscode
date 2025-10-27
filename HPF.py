import numpy as np
import matplotlib.pyplot as plt

# Filter parameters
fc= 0.3
N=11# cutoff frequency, filter length
m=np.arange(N)

# Generate high-pass filter coefficients using np.hamming
h = np.sinc(m - (N-1)/2) - 2 * fc * np.sinc(2 * fc * (m - (N-1)/2))
h *= np.hamming(N)  # Apply Hamming window
h /= np.sum(h)      # Normalize

print("FIR High-pass filter coefficients:")
print([f"{x:.6f}" for x in h])

w = np.linspace(0, np.pi, 512)
# Zero-pad the filter to 1024 points
h_padded = np.concatenate([h, np.zeros(1024 - len(h))])
# Compute FFT
H_fft = np.fft.fft(h_padded)
# Take first half and get magnitude
H = np.abs(H_fft[:512])
  

plt.figure(figsize=(8,4))
plt.plot(w/np.pi, H)
plt.title('Frequency Response of FIR High-Pass Filter')
plt.xlabel('Normalized Frequency (×π rad/sample)')
plt.ylabel('Magnitude')
plt.grid(True)
plt.show()