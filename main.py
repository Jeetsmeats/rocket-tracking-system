# Imports
import numpy as np
import matplotlib.pyplot as plt

# Import SoapySDR SDR Support Library
import SoapySDR
from SoapySDR import *          #SOAPY_SDR_ constants

# Import Modules
from HackRF import HackRF

def main():
    
    # Enumerate over visible devices
    results = SoapySDR.Device.enumerate()

    # Print the SoapySDR Results
    for result in results: 
        print(result)
    
    if input("Correct HackRF's? (Y/N) ").lower() == "y" or input("Correct HackRF's? (Y/N) ").lower() == "yes":
        
        # Create an instance of each hackrf
        hackrf_1 = HackRF("HackRF A", "0000000000000000675c62dc335c76cf")
        hackrf_2 = HackRF("HackRF B", "0000000000000000675c62dc302745cf")
        hackrf_3 = HackRF("HackRF C", "0000000000000000675c62dc304807cf")
        # hackrf_4 = HackRF("HackRF D", "0000000000000000################")

        sdr = {
            hackrf_1.get_name(): hackrf_1,
            hackrf_2.get_name(): hackrf_2,
            hackrf_3.get_name(): hackrf_3,
            # hackrf_4.get_name(): hackrf_4,
        }

        # HackRF Streams
        streams = []

        # Retrieve device information for each detected HackRF
        for device in sdr:
            
            # Retrieve selected HackRF
            hackrf = sdr[device].get_board()
            
            # Get current board settings
            fq_range = hackrf.getFrequencyRange(SOAPY_SDR_RX, 0) 
            ant_det = hackrf.listAntennas(SOAPY_SDR_RX, 0)
            
            # Print settings
            print(f'\nHACKRF DEVICE: {device}\n',
                '------------------------------')
            print(f'Frequency Range: {fq_range}')
            print(f'Antenna Details: {ant_det}')
            
            # Apply settings
            hackrf.setSampleRate(SOAPY_SDR_RX, 0, 20e6)
            hackrf.setFrequency(SOAPY_SDR_RX, 0, 9.15e6)

            # Setup a stream (complex floats)
            stream = hackrf.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF64)
            streams.append(stream)

            # Start streaming 
            hackrf.activateStream(stream)
            
            # Create a re-usable buffer for rx samples (Pre-allocate Memory)
            buff = np.array([0]*1024, np.complex64)

            print(f'Samples from {device}')
            # Retrieve 10 samples
            for i in range(10):
                
                samples = hackrf.readStream(stream, [buff], len(buff))
                
                print(samples) # num samples or error code
                
            # Close the stream
            hackrf.deactivateStream(stream) #stop streaming
            hackrf.closeStream(stream)
            
if __name__ == "__main__":
    main()