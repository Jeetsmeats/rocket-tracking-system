from pyhackrf2 import HackRF
from pylab import *
import numpy as np
import math
from time import sleep

# def pipe(data: bytes) -> bool:
#     a = np.array(data).astype(np.int8)
#     print(f"a: {a}")
#     print(a.shape)
#     return False    # pipe function may return True to stop rx immediately

# connect to both hackrfs
hackrf1 = HackRF(device_index = 0)
hackrf2 = HackRF(device_index = 1)

# confirm that the serial numbers are correct
hackrf1.get_serial_no()
hackrf2.get_serial_no()

# take 131072 samples from both (arbitrary value, this is the default number)
num_samples = 4096
hackrf1.sample_rate = 20e6
hackrf1.center_freq = 912e6
hackrf2.sample_rate = 20e6
hackrf2.center_freq = 912e6
samples1 = hackrf1.read_samples(num_samples)
samples2 = hackrf2.read_samples(num_samples)

'''hackrf.sample_count_limit = 2 * 10 ** 6
hackrf.start_rx(pipe_function=pipe)
sleep(0.1)
hackrf.stop_rx()

samples = hackrf.read_samples(hackrf.sample_count_limit)'''

# plot PSD of both to confirm we are getting sensible results (peak at 912 MHz, graphs are not exactly the same)
psd(samples1, NFFT=4096, Fs=hackrf1.sample_rate/1e6, Fc=hackrf1.center_freq/1e6)
xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')

figure()
psd(samples2, NFFT=4096, Fs=hackrf2.sample_rate/1e6, Fc=hackrf2.center_freq/1e6)
xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')

# lets plot time series 
# sampling times (assuming first sample is at t=0)
t = linspace(0, (num_samples-1)/hackrf1.sample_rate, num_samples)
# real and imaginary components of both samples
real_array_1 = real(samples1)
imag_array_1 = imag(samples1)
real_array_2 = real(samples2)
imag_array_2 = imag(samples2)

# plot Q time-series
figure()
plot(t, imag_array_2)
plot(t, imag_array_1)
xlabel("Seconds")
ylabel("Imaginary Value")
title("Q Time Series")

# plot I time-series
figure()
plot(t, real_array_2)
plot(t, real_array_1)
xlabel("Seconds")
ylabel("Real Value")
title("I Time Series")

# IQ constellation
figure()
scatter(real_array_1[30000:100000], imag_array_1[30000:100000])
scatter(real_array_2[30000:100000], imag_array_2[30000:100000])
xlabel("Real")
ylabel("Imaginary")
title("IQ Constellation")

show()
show()
show()
show()
show()
hackrf1.stop_rx()
hackrf2.stop_rx()