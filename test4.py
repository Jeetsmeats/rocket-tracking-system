import numpy as np
from pyhackrf2 import HackRF
from multiprocessing import Process
from time import time

def read_hackrf(hackrf):
    
    # Configure HackRF
    hackrf.sample_rate = int(10e6)
    hackrf.centre_freq = int(915e6)

    samples1 = hackrf.read_samples(8192)
    
    print(samples1)
    
def main():
    
    # Configuration
    center_freq = 915e6     # 915 MHz
    sample_rate = 10e6      # 10 MS/s
    num_samples = 8192      # Number of samples to read at once
    
    hackrf1 = HackRF(device_index = 0)
    hackrf2 = HackRF(device_index = 1)
    
    hackrf1.center_freq = center_freq
    hackrf2.center_freq = center_freq
    
    hackrf1.sample_rate = sample_rate
    hackrf2.sample_rate = sample_rate
    
    hackrf1.num_samples = num_samples
    hackrf2.num_samples = num_samples
    
    start = time()
    
    # Process for HackRF 0
    process1 = Process(target=read_hackrf, args=(hackrf1, ))

    # Process for HackRF 1
    process2 = Process(target=read_hackrf, args=(hackrf2, ))

    # Start the threads
    process1.start()
    process2.start()

    # Wait for both threads to complete
    process1.join()
    process2.join()

    end = time()
    print(f'This process took {end - start} seconds.')
    
if __name__ == "__main__":
    main()