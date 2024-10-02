import numpy as np
import matplotlib.pyplot as plt
import orjson

# Parameters for the time series
fs = 1000  # Sampling frequency (Hz)
t_end = 1  # Duration of the time series (seconds)
f_signal = 50  # Frequency of the sinusoid (Hz)
amplitude = 1  # Amplitude of the sinusoid
noise_power = 0.5  # Noise power (variance of the Gaussian noise)

# Generate time axis
t = np.linspace(0, t_end, int(fs * t_end), endpoint=False)

# Generate sinusoidal signal
signal = amplitude * np.sin(2 * np.pi * f_signal * t)

# Add Gaussian noise
noise = np.sqrt(noise_power) * np.random.randn(len(t))
noisy_signal = signal + noise

# Compute the FFT
nfft = len(noisy_signal)  # FFT size
fft_result = np.fft.fft(noisy_signal, nfft)
fft_freqs = np.fft.fftfreq(nfft, 1/fs)

# Find the index of the sinusoid frequency (f_signal)
index = np.argmin(np.abs(fft_freqs - f_signal))

# Retrieve the complex value of the frequency component at f_signal
complex_value = fft_result[index]
real_part = complex_value.real
imaginary_part = complex_value.imag

# Prepare the JSON object
frequency_data = {
    "frequency": str(f_signal),
    "real": str(real_part),
    "imaginary": str(imaginary_part),
    "data": str(complex_value)
}

# Convert to JSON using orjson
json_output = orjson.dumps(frequency_data, option=orjson.OPT_INDENT_2).decode()

# Print the JSON output
print(json_output)

# Take only the positive frequencies for plotting
positive_freqs = fft_freqs[:nfft // 2]
positive_fft_result = fft_result[:nfft // 2]

# Plot the time series data
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t, noisy_signal)
plt.title("Noisy Sinusoidal Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)

# Plot the FFT result (Magnitude)
plt.subplot(2, 1, 2)
plt.plot(positive_freqs, 2.0 / nfft * np.abs(positive_fft_result))
plt.title("FFT of Noisy Signal")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid(True)

# Show the plots
plt.tight_layout()
plt.show()