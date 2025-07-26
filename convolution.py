import numpy as np

x = np.array([1, 2, 3, 4, 5])
h = np.array([1, 0, 0, 0, 0])

class Convolution:
    def __init__(self, x, h):
        self.x = x
        self.h = h
    
    @staticmethod
    def dft(x):
        """
        Compute the Discrete Fourier Transform (DFT) of a 1D signal.
        
        Parameters:
        signal (array-like): Input signal to transform.
        
        Returns:
        np.ndarray: DFT of the input signal.
        """
        N = len(x)
        n = np.arange(N)
        k = n.reshape((N, 1))
        exp_term = np.exp(-2j * np.pi * k * n / N)
        res = np.dot(exp_term, x)
        return res
   
    @staticmethod
    def convolve(x, h):
        """to perform convolution by multiplying the DFTs of the 
        two signals in the frequency domain and then taking the IDFT of the result."""
        X = Convolution.dft(x)
        H = Convolution.dft(h)
        Y = X * H  # Element-wise multiplication
        return Convolution.idft(Y)
    
    @staticmethod
    def idft(X):
        """
        Compute the Inverse Discrete Fourier Transform (IDFT) of a 1D signal.

        Parameters:
        X (array-like): Input signal in frequency domain to transform.

        Returns:
        np.ndarray: IDFT of the input signal.
        """
        N = len(X)
        n = np.arange(N)
        k = n.reshape((N, 1))
        exp_term = np.exp(2j * np.pi * k * n / N)
        res = np.dot(exp_term, X) / N
        return res

result = Convolution.convolve(x, h)
print("Convolution result:", result)