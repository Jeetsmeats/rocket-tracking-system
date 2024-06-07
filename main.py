# Imports
import numpy as np
from numpy.fft import fft
import matplotlib.pyplot as plt

# Import SoapySDR SDR Support Library
import SoapySDR
from SoapySDR import *          #SOAPY_SDR_ constants

# Import Modules
from HackRF import HackRF

def argand(input, ax):
    """_summary_
    
    Plot an argand diagram
    Args:
        input (_type_): _description_
    """
    max = np.max(np.ceil(np.absolute(input)))
    for x in range(len(input)):
        
        val = input[x] / max
        ax.plot([0,val.real],[0,val.imag],'r.',markersize=2)
    
    limit = 0.25 # set limits for axis
    ax.set_xlim((-limit,limit))
    ax.set_ylim((-limit,limit))
    ax.set_ylabel('Imaginary')
    ax.set_xlabel('Real')
        
    # ax.show()
            

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
    num_samples = 5000              # Number of samples
    num_plot_samples = 5            # Number of samples to plot
    num_dpoints = 1024 * 1          # Number of IQ datapoints
    num_devices = len(sdr)          # Number of connected devices
    chan = 0                        # Channel
    center_freq = 900e6             # Center Frequency
    bw = 10e6                       # Bandwidth
    sample_rate = 10e6              # Sample Rate
    
    ## Variables    
    streams = []                                                                        # List of HackRF Streams
    
    freq = np.arange(-sample_rate/2,  sample_rate/2, sample_rate/num_dpoints)           # Frequency
    # freq += center_freq
    
    data = np.empty((num_devices, num_samples, num_dpoints), np.complex64)              # Raw Data
    fft_out = data                                                                      # FFT Values
    phase_out = data                                                                    # Phase Data
    
    ## Retrieve HackRF device information
    for n_device, device in enumerate(sdr):
                
        # Retrieve selected HackRF
        hackrf = sdr[device].get_board()
        
        # Apply settings
        hackrf.setSampleRate(SOAPY_SDR_RX, chan, sample_rate)
        hackrf.setFrequency(SOAPY_SDR_RX, chan, center_freq)
        hackrf.setBandwidth(SOAPY_SDR_RX, chan, bw)
        
        # Get current board settings
        fq_range = hackrf.getFrequencyRange(SOAPY_SDR_RX, 0) 
        ant_det = hackrf.listAntennas(SOAPY_SDR_RX, 0)
        bw_det = hackrf.getBandwidth(SOAPY_SDR_RX, 0)
        
        # Print settings
        print(f'\nHACKRF DEVICE: {device}\n',
            '------------------------------')
        print(f'Frequency Range: {fq_range[0].minimum()}-{fq_range[0].maximum()}')
        print(f'Antenna Details: {ant_det}')
        print(f'Bandwidth Details: {bw_det}')

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
                        
            # Retrieve device information for each detected HackRF
            for n_device, device in enumerate(sdr):
                
                # Retrieve selected HackRF
                hackrf = sdr[device].get_board()
                hackrf.readStream(stream, [buff], len(buff))
                
                data[n_device][i] = buff / num_dpoints
                fft_out[n_device][i] = fft(buff) / num_dpoints
                    
            buff = np.array([0]*num_dpoints, np.complex64) 

    except Exception as e:
        print(f'The following error was found: {e}')
    finally:
    
        # Add samples to data stack
        print(f'\nDevice {n_device}\ndata: {data[n_device]}')            
        print("---------------------------------\n")
            
    for n_device, device in enumerate(sdr):
        
            # Close the stream
            hackrf.deactivateStream(streams[n_device])                 # stop streaming
            hackrf.closeStream(streams[n_device])
    
    ## Figures
    fig, ax = plt.subplots(num_plot_samples, num_devices, constrained_layout=True)
    
    for device_num in range(num_devices): 
        for plot_sample_num,sample_num in enumerate(range((num_samples - num_plot_samples), num_samples)):
            
            axis = ax[plot_sample_num][device_num]
            
            x = data[device_num][sample_num]
            argand(x, axis)
        
            # Plot Labels
            ax[plot_sample_num][device_num].set_title(f'{sdr_key[device_num]} (Sample {sample_num + 1})')
            ax[plot_sample_num][device_num].set_xlabel('f(Hz)')
            ax[plot_sample_num][device_num].set_ylabel('Mag')
            
            # # Get the IQ values
            # out = fft_out[device_num][sample_num]                                  # FFT
            
            # ax[plot_sample_num][device_num].plot(freq, np.abs(out), color='blue')       # Plot FFTq - sample_rate/2
            
            # # Grid Lines
            # ax[plot_sample_num][device_num].grid(which='major', color='#DDDDDD', linewidth=0.8)
            # ax[plot_sample_num][device_num].grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
            
    plt.show()
    
    
if __name__ == "__main__":
    main()