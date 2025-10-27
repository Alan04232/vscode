import numpy as np
import matplotlib.pyplot as plt

# Filter parameters
fc, N = 0.3, 11  # cutoff frequency, filter length

# Generate filter coefficients using np.hamming
h = 2 * fc * np.sinc(2 * fc * (np.arange(N) - (N-1)/2))
h *= np.hamming(N)  # Apply Hamming window
h /= np.sum(h)      # Normalize

print("FIR coefficients:")
print([f"{x:.6f}" for x in h])

# Frequency response
w = np.linspace(0, np.pi, 512)
H = np.abs(np.fft.fft(h, 1024)[:512])  # Using FFT for efficiency

plt.figure(figsize=(8,4))
plt.plot(w/np.pi, H)
plt.title('FIR Low-Pass Filter Response')
plt.xlabel('Normalized Frequency (×π rad/sample)')
plt.ylabel('Magnitude')
plt.grid(True)
plt.show()