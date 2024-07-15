from pyhackrf2 import HackRF
from pylab import *
import numpy as np
from numpy.fft import fft, fftshift
from time import sleep
import pandas as pd

def pipe(data):
    
    values = np.array(data).astype(np.int8)
    iq = values.astype(np.float64).view(np.complex128)
    
    print(iq)
    
hackrf1 = HackRF(device_index=0)
hackrf2 = HackRF(device_index=1)

print(hackrf1.get_serial_no())
print(hackrf2.get_serial_no()) 
# take 131072 samples from both (arbitrary value, this is the default number)

num_samples = 10 ** 5
hackrf1.sample_rate = 20e6
hackrf1.center_freq = 915e6
hackrf2.sample_rate = 20e6
hackrf2.center_freq = 915e6
samples1 = hackrf1.read_samples(num_samples)
samples2 = hackrf2.read_samples(num_samples)

# hackrf1.start_rx(pipe_function=pipe)
# hackrf2.start_rx(pipe_function=pipe)

# sleep(5)
# hackrf1.stop_tx()
# hackrf2.stop_tx()

data = pd.DataFrame({"Phase Difference": []})
phase_diff = []


for i in range(50):
    samples1 = hackrf1.read_samples(num_samples)
    samples2 = hackrf2.read_samples(num_samples)
    
    out1 = fft(samples1)
    out2 = fft(samples2)
    
    complex_1 = out1[0]
    complex_2 = out2[0]
    
    phase_1 = np.arctan2(complex_1.imag, complex_1.real)
    phase_2 = np.arctan2(complex_2.imag, complex_2.real)
    
    phase_diff.append(phase_1 - phase_2)
    
data["Phase Difference"] = phase_diff
data.to_csv("Phase Values")


# print(samples2)
# t = linspace(0, (num_samples - 1) / hackrf1.sample_rate, num_samples)

# # real and imaginary components of both samples
# real_array_1 = real(samples1)
# imag_array_1 = imag(samples1)
# real_array_2 = real(samples2)
# imag_array_2 = imag(samples2)

# figure()
# plot(t, real_array_2)
# plot(t, real_array_1)
# xlabel("Seconds")
# ylabel("Real Value")
# title("I Time Series - Parallel Clock")

# figure()
# plot(t, imag_array_2)
# plot(t, imag_array_1)
# xlabel("Seconds")
# ylabel("Imag Value")
# title("Q Time Series - Parallel Clock")

# figure()
# scatter(real_array_1, imag_array_1)
# scatter(real_array_2, imag_array_2)
# xlabel("Real")
# ylabel("Imaginary")
# title("IQ Constellation - Parallel Clock")

# show()
# show()
# show()