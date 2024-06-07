# Imports
import numpy as np
from numpy.fft import fft
 
# Import SoapySDR SDR Support Library
import SoapySDR
from SoapySDR import *          #SOAPY_SDR_ constants

class Processing(object):
    """_summary_

    Args:
        object (_type_): _description_
    """
    
    def __init__(self, 
                 sdr, 
                 NUM_SAMPLES, 
                 N, 
                 NUM_DEVICES, 
                 CHANNEL, 
                 CENTER_FREQ, 
                 BANDWIDTH,
                 SAMPLE_RATE,
                 res_factor
                 ):
        """_summary_

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
        self.N = N * res_factor                  # Number of IQ datapoints
        self.NUM_DEVICES = NUM_DEVICES              # Number _summary_of connected devices
        self.CHANNEL = CHANNEL                      # Antenna Channel
        self.CENTRE_FREQ = CENTER_FREQ              # Center Frequency
        self.BANDWIDTH = BANDWIDTH                  # Bandwidth (Maximum bandwidth)
        self.SAMPLE_RATE = SAMPLE_RATE              # Sample Rate (Maximum Sample Rate)

        self.sdr = sdr                              # SDR Dictionary
        
        ## Variables
        self.streams = []                                                                                # List of HackRF Streams
        
        freq = np.arange(-self.SAMPLE_RATE/2,  self.SAMPLE_RATE/2, self.SAMPLE_RATE/self.N)
        data = np.empty((self.NUM_DEVICES, self.NUM_SAMPLES, self.N), np.complex64)                                # Raw Data
        buff = np.zeros(self.N, np.complex64)                                                            # Re-usable Buffer
        fft_out = data                                                                              # FFT Values
        phase_out = data                                                                            # Phase Data
        
        # Retrieve device information for each detected HackRF
        for n_device, device in enumerate(self.sdr):
            
            ## HackRF Settings
            # Retrieve sele devcted HackRF
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
        """
        # Retrieve device information for each detected HackRF
        for device_num, hackRF in enumerate(self.sdr):
            
            # Deactivate the stream
            hackRF.deactivateStream(self.streams[device_num])
            
