# Imports
import matplotlib.pyplot as plt

# Import SoapySDR SDR Support Library
import SoapySDR
from SoapySDR import *          #SOAPY_SDR_ constants

# Import Modules
from HackRF import HackRF
from Processor import Processor
from Visualiser import Visualiser                    

def main():
    """_summary_
    Main function for running RTS
    """
    
    ## Constants   
    NUM_SAMPLES = 5000              # Number of samples
    PLOT_SAMPLES = 5                # Number of samples to plot
    N = 1024                        # Number of IQ data points
    NUM_DEVICES = len(sdr)          # Number of connected devices
    CHANNEL = 0                     # Antenna channel
    CENTRE_FREQ = 900e6             # Center Frequency
    BANDWIDTH = 10e6                # Bandwidth
    SAMPLE_RATE = 10e6              # Sample Rate
    
    ## HackRF Boards
    # Default HackRF Instances
    hackrf_1 = HackRF("HackRF A", "0000000000000000675c62dc335c76cf")
    hackrf_2 = HackRF("HackRF B", "0000000000000000675c62dc302745cf")
    hackrf_3 = HackRF("HackRF C", "0000000000000000675c62dc304807cf")
    # hackrf_4 = HackRF("HackRF D", "0000000000000000################")

    # SDR Dictionary
    sdr = {
        hackrf_1.get_name(): hackrf_1,
        hackrf_2.get_name(): hackrf_2,
        # hackrf_3.get_name(): hackrf_3,
        # hackrf_4.get_name(): hackrf_4,
    }
    
    # Board Names
    BOARD_NAMES = [board_name for board_name in sdr]    
    
    ## Functional objects
    # Processing Unit
    processor = Processor(
        sdr,
        NUM_SAMPLES,
        N,
        NUM_DEVICES,
        CHANNEL,
        CENTRE_FREQ,
        BANDWIDTH,
        SAMPLE_RATE,
        1
    )

    # Data Visualisation Unit
    visuals = Visualiser(
        PLOT_SAMPLES, NUM_DEVICES, NUM_SAMPLES, BOARD_NAMES
    )
    
    ## Data objects
    
    ## Main Logic
    # while True:
    #     pass
    
    
    processor.activate_boards()
    processor.collect_samples()
    processor.deactivate_boards()     
    
    visuals.create_figure("IQ Constellation")
    visuals.create_figure("FFT Plot")
    
    visuals.plot_argand_diagram("IQ Constellation", )
    visuals.plot_fft("FFT Plot", )
        
    
if __name__ == "__main__":
    main()