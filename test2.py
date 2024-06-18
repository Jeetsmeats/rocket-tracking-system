from pyhackrf2 import HackRF
from pylab import *
import numpy as np
from time import sleep

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

print(samples1)
print(samples2)
t = linspace(0, (num_samples - 1) / hackrf1.sample_rate, num_samples)
# real and imaginary components of both samples
real_array_1 = real(samples1)
imag_array_1 = imag(samples1)
real_array_2 = real(samples2)
imag_array_2 = imag(samples2)

figure()
plot(t, real_array_2)
plot(t, real_array_1)
xlabel("Seconds")
ylabel("Real Value")
title("I Time Series - Parallel Clock")

figure()
plot(t, imag_array_2)
plot(t, imag_array_1)
xlabel("Seconds")
ylabel("Imag Value")
title("Q Time Series - Parallel Clock")

figure()
scatter(real_array_1, imag_array_1)
scatter(real_array_2, imag_array_2)
xlabel("Real")
ylabel("Imaginary")
title("IQ Constellation - Parallel Clock")

show()
show()
show()