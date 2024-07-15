from multiprocessing import Process
import time
from pyhackrf2 import HackRF
from pylab import *
import numpy as np
import math


num_samples = 131072

def task1(hackrf):
    
    print("Task 1 started")
    time.sleep(2)
    

    #samples1 = hackrf.read_samples(num_samples)
    print("Task 1 finished")

def task2(hackrf):
    
    print("Task 2 started")
    time.sleep(2)


    #samples2 = hackrf.read_samples(num_samples)
    print("Task 2 finished")

if __name__ == "__main__":
    
    hackrf1 = HackRF(device_index = 0)
    hackrf2 = HackRF(device_index = 1)
    hackrf1.sample_rate = 20e6
    hackrf1.center_freq = 912e6
    hackrf2.sample_rate = 20e6
    hackrf2.center_freq = 912e6
    # Create processes
    process1 = Process(target=task1, args=(hackrf1,))
    process2 = Process(target=task2, args=(hackrf2,))

    # Start processes
    process1.start()
    process2.start()

    # Wait for both processes to complete
    process1.join()
    process2.join()

    print("Both tasks are done")
    '''
    real_array_1 = real(samples1)
    imag_array_1 = imag(samples1)
    real_array_2 = real(samples2)
    imag_array_2 = imag(samples2)
    t = linspace(0, (num_samples-1)/hackrf1.sample_rate, num_samples)
    figure()
    plot(t, imag_array_2)
    plot(t, imag_array_1)
    xlabel("Seconds")test_745cf_v2.raw
    ylabel("Imaginary Value")
    title("Q Time Series")

    # plot I time-series
    figure()
    plot(t, real_array_2)
    plot(t, real_array_1)
    xlabel("Seconds")
    ylabel("Real Value")
    title("I Time Series")
    
    show()
    show()'''