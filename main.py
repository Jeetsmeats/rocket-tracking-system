# Imports
import matplotlib.pyplot as plt
import keyboard
import time

# Import Modules
from HackRF import HackRF
from Processor import Processor
from Visualiser import Visualiser                    
from FFT import FFT

def main():
    """_summary_
    Main function for running RTS
    """
    
    ## HackRF Boards
    # Default HackRF Instances
    hackrf_1 = HackRF("HackRF A", "0000000000000000675c62dc335c76cf")
    hackrf_2 = HackRF("HackRF B", "0000000000000000675c62dc302745cf")
    hackrf_3 = HackRF("HackRF C", "0000000000000000675c62dc304807cf")
    # hackrf_4 = HackRF("HackRF D", "0000000000000000################")
    
    # SDR Dictionary
    sdr = {    ## Main Logic
        hackrf_1.get_name(): hackrf_1,
        hackrf_2.get_name(): hackrf_2,
        # hackrf_3.get_name(): hackrf_3,
        # hackrf_4.get_name(): hackrf_4,
    }
    
    ## Constants   
    NUM_SAMPLES = 5000              # Number of samples
    PLOT_SAMPLES = 5                # Number of samples to plot
    N = 1024                        # Number of IQ data points
    NUM_DEVICES = len(sdr)          # Number of connected devices
    CHANNEL = 0                     # Antenna channel
    CENTRE_FREQ = 915e6           # Center Frequency
    BANDWIDTH = 10e6                # Bandwidth
    SAMPLE_RATE = 10e6              # Sample Rate

    # Board Names
    BOARD_NAMES = [board_name for board_name in sdr]    
    
    is_collecting_samples = input("Collect samples? [y]/[n] ")
    
    if is_collecting_samples == "y" or is_collecting_samples == "yes":
        
        # Processing Unit
        processor = Processor(
            sdr,
            N,
            NUM_DEVICES,
            CHANNEL,
            CENTRE_FREQ,
            BANDWIDTH,
            SAMPLE_RATE,
            NUM_SAMPLES
        )

        # Data Visualisation Unit
        visuals = Visualiser(
            NUM_DEVICES,
            N,
            SAMPLE_RATE,
            BOARD_NAMES,
            PLOT_SAMPLES,
            NUM_SAMPLES
        )
        
        ## Processing 
        processor.activate_boards()
        
        fft = processor.collect_samples()
        data = processor.get_data()
        freq = processor.get_frequency()

        fft_sample = fft.get_fft_sample()
        
        processor.deactivate_boards()   
        
        visuals.plot_IQ_constellation("IQ",data)
        visuals.plot_fft("FFT",fft_sample, freq)
        visuals.plot_psd("PSD",fft_sample, freq)
        
    else:
        
        # Processing Unit
        processor = Processor(
            sdr,
            N,
            NUM_DEVICES,
            CHANNEL,
            CENTRE_FREQ,
            BANDWIDTH,
            SAMPLE_RATE,
        )

        # Data Visualisation Unit
        visuals = Visualiser(
            NUM_DEVICES,
            N,
            SAMPLE_RATE,
            BOARD_NAMES,
        )
        
        ## Processing 
        freq = processor.get_frequency()
        
        processor.activate_boards()
        
        print("Begin streaming.")
        print("----------------")
        # LOOP FOR REAL TIME TRACKING
        while True:
            
            
            fft = processor.sample()
            data = processor.get_data()

            fft_sample = fft.get_fft_sample()
            
            visuals.plot_all("Real time RF data", fft_sample, data, freq)
            if keyboard.is_pressed('q'):
                
                print("Exiting stream.")
                print("----------------")
                
                break
            
        processor.deactivate_boards()   

if __name__ == "__main__":
    main()