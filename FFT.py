# Imports
import numpy as np
from numpy.fft import fft

class FFT(object):
    
    def __init__(self, NUM_DEVICES, N, SAMPLE_RATE, NUM_SAMPLES=None):
        """_summary_

        Args:
            NUM_DEVICES (_type_): _description_
            N (_type_): _description_
            SAMPLE_RATE (_type_): _description_
            NUM_SAMPLES (int, optional): _description_. Defaults to None.
        """
        
        # Properties
        self.N = N
        self.SAMPLE_RATE = SAMPLE_RATE
        
        if NUM_SAMPLES is not None:
            
             # Initialise FFT variable for real-time stream
            self.samples = np.empty((NUM_DEVICES, N), np.complex64)
        else:
            
            # Initialise the FFT variable for simple sampling
            self.samples = np.empty((NUM_DEVICES, NUM_SAMPLES, N), np.complex64)                                     # Raw sample
        
    def set_fft_sample(self, buffer, num_device, num_sample=None):
        """_summary_

        Args:
            num_device (_type_): _description_
            num_sample (_type_): _description_
            buffer (_type_): _description_
        """
        
        if num_sample is not None:
            self.samples[num_device][num_sample] = fft(buffer)
        else:
            self.samples[num_device] = fft(buffer)

    def get_fft_sample(self):
        """_summary_

        Get the FFT sample.
        Returns:
            numpy.Array: FFT sample
        """
        return self.samples
    
    def get_desired_freq_sample(self):
        pass
    
    def get_euler_samples(self):
        pass