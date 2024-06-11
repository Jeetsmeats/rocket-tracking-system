# Imports
import numpy as np
from numpy.fft import fft
 
# Import SoapySDR SDR Support Library
import SoapySDR
from SoapySDR import *          #SOAPY_SDR_ constants

# Import modules
from FFT import FFT

class Processor(object):
    """_summary_

    Processing Unit for retrieving data from the SDR.
    """
    
    def __init__(self, 
                 sdr, 
                 NUM_SAMPLES, 
                 N, 
                 NUM_DEVICES, 
                 CHANNEL, 
                 CENTRE_FREQ, 
                 BANDWIDTH,
                 SAMPLE_RATE,
                 res_factor
                 ):
        """_summary_
        Initialise the processing unit.
        
        Args:
            sdr (_type_): _description_
            NUM_SAMPLES (_type_): _description_
            N (_type_): _description_
            NUM_DEVICES (_type_): _description_
            CHANNEL (_type_): _description_
            CENTER_FREQ (_type_): _description_
            BANDWIDTH (_type_): _description_
            SAMPLE_RATE (_type_): _description_
            res_factor (_type_): Factor to change the data point resolution.
        """
        
        ## Constants   
        self.NUM_SAMPLES = NUM_SAMPLES              # Number of samples
        self.N = N * res_factor                     # Number of IQ datapoints
        self.NUM_DEVICES = NUM_DEVICES              # Number _summary_of connected devices
        self.CHANNEL = CHANNEL                      # Antenna Channel
        self.CENTRE_FREQ = CENTRE_FREQ              # Center Frequency
        self.BANDWIDTH = BANDWIDTH                  # Bandwidth (Maximum bandwidth)
        self.SAMPLE_RATE = SAMPLE_RATE              # Sample Rate (Maximum Sample Rate)

        self.sdr = sdr                              # SDR Dictionary
        
        ## Variables
        self.streams = []                                                                                                    # List of HackRF Streams
        
        self.freq = np.arange(-self.SAMPLE_RATE / 2,  self.SAMPLE_RATE / 2, self.SAMPLE_RATE / self.N)                       # Frequencies
        self.freq += CENTRE_FREQ
        
        self.data = np.empty((self.NUM_DEVICES, self.NUM_SAMPLES, self.N), np.complex64)                                     # Raw Data
        self.fft = FFT(self.NUM_DEVICES, self.N, self.NUM_SAMPLES)                                                                                               # FFT Data

    def activate_boards(self):
        
        # Activate the board streams
        for device in self.sdr:
            
            ## HackRF Settings
            # Retrieve selected HackRF
            hackrf = self.sdr[device].get_board()
            
            # Apply settings
            hackrf.setSampleRate(SOAPY_SDR_RX, self.CHANNEL, self.SAMPLE_RATE)
            hackrf.setFrequency(SOAPY_SDR_RX, self.CHANNEL, self.CENTRE_FREQ)
            hackrf.setBandwidth(SOAPY_SDR_RX, self.CHANNEL, self.BANDWIDTH)
            
            # Get current board settings
            fq_range = hackrf.getFrequencyRange(SOAPY_SDR_RX, 0) 
            ant_det = hackrf.listAntennas(SOAPY_SDR_RX, 0)
            
            # Print settings
            print(f'\nHACKRF DEVICE: {device}\n',
                '------------------------------')
            print(f'Frequency Range: {fq_range[0].minimum()}-{fq_range[0].maximum()}')
            print(f'Antenna Details: {ant_det}')

            ## Stream Data
            # Setup a stream (complex floats)
            stream = hackrf.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
            self.streams.append(stream)

            # Start streaming 
            hackrf.activateStream(stream)
            
    def deactivate_boards(self):
        """_summary_
        
        Deactivate streaming for all SDR boards.
        """
        
        # Retrieve device information for each detected HackRF
        for device_num, board_name in enumerate(self.sdr):
            
            # Get the hackrf board
            hackRF = self.sdr[board_name].get_board()
            
            # Deactivate the stream
            hackRF.deactivateStream(self.streams[device_num])
    
    def run_stream(self):
        """_summary_
        
        Enable and run data streaming for the SDR boards.
        """
        pass
    
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
                    hackrf.readStream(self.streams[n_device], [buff], len(buff))
                    
                    self.data[n_device][i] = buff
                    self.fft.set_fft_sample(n_device, i, buff)
                        
                    buff = np.zeros(self.N, np.complex64) 

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