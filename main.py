# Imports
import numpy as np
from numpy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# Import SoapySDR SDR Support Library
import SoapySDR
from SoapySDR import *          #SOAPY_SDR_ constants

# Import Modules
from HackRF import HackRF

def main():

    ## OPTIONAL: Check Devices
    # check_devices = input("Check compatible devices? [y]/[n] ").lower()
    # if check_devices == "y" or check_devices == "yes":
        
    #     for result in SoapySDR.Device.enumerate(): print(result)
        
    ## HackRF Blocks
    # Default HackRF Instances
    hackrf_1 = HackRF("HackRF A", "0000000000000000675c62dc335c76cf")
    hackrf_2 = HackRF("HackRF B", "0000000000000000675c62dc302745cf")
    hackrf_3 = HackRF("HackRF C", "0000000000000000675c62dc304807cf")
    # hackrf_4 = HackRF("HackRF D", "0000000000000000################")

    sdr = {
        hackrf_1.get_name(): hackrf_1,
        hackrf_2.get_name(): hackrf_2,
        # hackrf_3.get_name(): hackrf_3,
        # hackrf_4.get_name(): hackrf_4,
    }
    
    sdr_key = list(sdr.keys())

    ## Constants   
    num_samples = 5                 # Number of samples
    num_dpoints = 1024 * 1          # Numer of IQ datapoints
    num_devices = len(sdr)          # Number of connected devices
    chan = 0                        # Channel
    center_freq = 100e6             # Center Frequency
    bw = 10e6                       # Bandwidth
    sample_rate = 20e6              # Sample Rate
    
    # Variables
    streams = []                    # List of HackRF Streams
    # t = np.arange(num_dpoints)
    freq = np.arange(-sample_rate/2,  sample_rate/2, sample_rate/num_dpoints)
    freq += center_freq
    
    # Data storage
    data = np.empty((num_devices, num_samples, num_dpoints), np.complex64)              # Raw Data
    fft_out = data                                                                      # FFT Values
    phase_out = data                                                                    # Phase Data
    
    ## Figures
    fig, ax = plt.subplots(num_samples, num_devices, constrained_layout=True)
    
    # Retrieve device information for each detected HackRF
    for n_device, device in enumerate(sdr):
        
        ## HackRF Settings
        # Retrieve sele devcted HackRF
        hackrf = sdr[device].get_board()
        
        # Apply settings
        hackrf.setSampleRate(SOAPY_SDR_RX, chan, sample_rate)
        hackrf.setFrequency(SOAPY_SDR_RX, chan, center_freq)
        hackrf.setBandwidth(SOAPY_SDR_RX, chan, bw)
        
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
        streams.append(stream)

        # Start streaming 
        hackrf.activateStream(stream)

        # Create a re-usable buffer for rx samples (Pre-allocate Memory)
        buff = np.array([0]*num_dpoints, np.complex64) 
        
        print(f'\nTaking samples from {device}....')
        try:
            
            # Retrieve 10 samples
            for i in range(num_samples):                    
                             
                info = hackrf.readStream(stream, [buff], len(buff))
                ret, flags, timeNs = info.ret, info.flags, info.timeNs
                
                # Store data
                if ret > 0 and not flags:
                    
                    data[n_device][i] = buff
                    fft_out[n_device][i] = fft(buff, norm="ortho")
                    
            # Close the stream
            hackrf.deactivateStream(stream)                 # stop streaming
            hackrf.closeStream(stream)
        except Exception as e:
            print(f'The following error was found: {e}')
        finally:
        
            # Add samples to data stack
            print(f'\nDevice {n_device}\ndata: {data[n_device]}')            
            print("---------------------------------\n")
    
    for device_num in range(num_devices):
        for sample_num in range(num_samples):
            
            # Get the IQ values
            out = fft_out[device_num][sample_num]                                  # FFT for single sample
                        
            # Plot Data
            ax[sample_num][device_num].plot(freq, np.abs(out), color='blue')       # Plot Q

            # Plot Labels
            ax[sample_num][device_num].set_title(f'{sdr_key[device_num]} (Sample {sample_num + 1})')
            ax[sample_num][device_num].set_xlabel('f(Hz)')
            ax[sample_num][device_num].set_ylabel('Mag')
            
            # Grid Lines
            ax[sample_num][device_num].grid(which='major', color='#DDDDDD', linewidth=0.8)
            ax[sample_num][device_num].grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
            
    # plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    main()