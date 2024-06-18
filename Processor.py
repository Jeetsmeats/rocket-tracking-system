# Imports
import numpy as np
from numpy.fft import fft

# Import modules
from FFT import FFT

class Processor(object):
    """_summary_

    Processing Unit for retrieving data from the SDR.
    """
    
    def __init__(self, 
                 sdr,
                 N, 
                 NUM_DEVICES, 
                 CHANNEL, 
                 CENTRE_FREQ, 
                 BANDWIDTH,
                 SAMPLE_RATE,
                 NUM_SAMPLES=None
                 ):
        """_summary_

        Args:
            sdr (_type_): _description_
            N (_type_): _description_
            NUM_DEVICES (_type_): _description_
            CHANNEL (_type_): _description_
            CENTRE_FREQ (_type_): _description_
            BANDWIDTH (_type_): _description_
            SAMPLE_RATE (_type_): _description_
            NUM_SAMPLES (_type_, optional): _description_. Defaults to None.
        """
        
        ## Constants   
        if NUM_SAMPLES is not None:
            self.NUM_SAMPLES = NUM_SAMPLES              # Number of samples
            
        self.N = N                                  # Number of IQ datapoints
        self.NUM_DEVICES = NUM_DEVICES              # Number _summary_of connected devices
        self.CHANNEL = CHANNEL                      # Antenna Channel
        self.CENTRE_FREQ = CENTRE_FREQ              # Center Frequency
        self.BANDWIDTH = BANDWIDTH                  # Bandwidth (Maximum bandwidth)
        self.SAMPLE_RATE = SAMPLE_RATE              # Sample Rate (Maximum Sample Rate)

        self.sdr = sdr                              # SDR Dictionary                                                                                                  # List of HackRF Streams
        
        self.freq = np.arange(-self.SAMPLE_RATE / 2,  self.SAMPLE_RATE / 2, self.SAMPLE_RATE / self.N)                       # Frequencies
        self.freq += CENTRE_FREQ
                
        if NUM_SAMPLES is not None:             # Sampling
            
            self.fft = FFT(self.NUM_DEVICES, self.N, self.SAMPLE_RATE, self.NUM_SAMPLES)                                     # FFT Data
            self.data = np.empty((self.NUM_DEVICES, self.NUM_SAMPLES, self.N), np.complex64)                                 # Raw Data
        else:                                   # Streaming
            self.fft = FFT(self.NUM_DEVICES, self.N, self.SAMPLE_RATE)                                                       # FFT Data
            self.data = np.empty((self.NUM_DEVICES, self.N), np.complex64)                                                   # Raw Data
            
    def activate_boards(self):
        
        # Activate the board streams
        for device in self.sdr:
            
            ## HackRF Settings
            # Retrieve selected HackRF
            hackrf = self.sdr[device].get_board()
            
            hackrf.sample_rate = self.SAMPLE_RATE
            hackrf.center_freq = self.CENTRE_FREQ
        
    def sample(self):
        """_summary_
        
        Enable and run data streaming for the SDR boards.
        """
        buff = np.zeros(self.N, np.complex128)                                                 # Re-usable Buffer
        
        try:              
                    
            for n_device, device in enumerate(self.sdr):
                
                # Retrieve selected HackRF
                hackrf = self.sdr[device].get_board()
                buff = hackrf.read_samples(self.N)
                
                self.data[n_device] = buff
                self.fft.set_fft_sample(buff, n_device)
                
                buff = np.zeros(self.N, np.complex128)                                                 # Re-usable Buffer
        except Exception as e:
            
            print(f'The following error was found: {e}')
        finally:
                        
            return self.fft
    
    def collect_samples(self):
        """_summary_
        
        Collect a specific number of samples
        """
        
        buff = np.zeros(self.N, np.complex64)                                                 # Re-usable Buffer
        
        try:
    
            # Retrieve 10 samples
            for i in range(self.NUM_SAMPLES):                    
                    
                for n_device, device in enumerate(self.sdr):
                    
                    # Retrieve selected HackRF
                    hackrf = self.sdr[device].get_board()
                    buff = hackrf.read_samples(self.N)
                    
                    self.data[n_device][i] = buff
                    self.fft.set_fft_sample(buff, n_device, i)
                        
                    buff = np.zeros(self.N, np.complex128)                                                 # Re-usable Buffer

        except Exception as e:
            
            print(f'The following error was found: {e}')
        finally:
                        
            return self.fft
        
    def get_frequency(self):
        """_summary_

        Get the frequency values
        
        Returns:
            Numpy.Array: Frequency range
        """
        
        return self.freq
    
    def get_data(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.data
    
    def get_fft(self):
        
        return self.fft