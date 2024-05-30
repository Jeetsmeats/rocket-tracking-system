# Imports
import numpy as np
import matplotlib.pyplot as plt

# Import SoapySDR SDR Support Library
import SoapySDR
from SoapySDR import *          #SOAPY_SDR_ constants

def main():
    pass

if __name__ == "main":
    pass

# Enumerate over visible devices
# results = SoapySDR.Device.enumerate()

# # Print the SoapySDR Results
# for result in results: 
#     print(result)
    
# Create a Driver Instance
arg1 = dict(driver="hackrf", serial="0000000000000000675c62dc335c76cf")
arg2 = dict(driver="hackrf", serial="0000000000000000675c62dc302745cf")
# arg3 = dict(driver="hackrf", serial="0000000000000000675c62dc304807cf")
# arg4 = dict(driver="hackrf", serial="0000000000000000")

# Create an instance of each hackrf
hackrf_A = SoapySDR.Device(arg1)
hackrf_B = SoapySDR.Device(arg2)
# hackrf_C = SoapySDR.Device(arg3)
# hackrf_D = SoapySDR.Device(arg4)

sdr = {
    'HackRF A': hackrf_A,
    'HackRF B': hackrf_B,
    # 'HackRF C': hackrf_C,
    # 'HackRF D': hackrf_D,
}

# HackRF Streams
streams = []

# Retrieve device information for each detected HackRF
for device in sdr:
    
    # Retrieve selected HackRF
    hackrf = sdr[device]
    
    print(hackrf.getDriverKey())
    # Print hackrf board settings
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

    # Setup hackrf stream
    rx_stream = hackrf.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF64)
    streams.append(rx_stream)
