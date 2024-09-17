import numpy as np
from numpy.fft import fft
from matplotlib import pyplot as plt
import paho.mqtt.client as paho
import subprocess
import os

# Constants
fs = 10 * 10**6  # sample rate
K = 4096 * 2  # number of samples real + imaginary per time step
fd = 1e6  # frequency of data
c = 3e8  # speed of light
M = 2  # number of arrays
R = 0.08  # half the distance between the two arrays
CarrierFreq = 915e6  # 915 MHz
WidthofBeams = 60  # width of the beams
Lamda = c / CarrierFreq  # wavelength of Signal frequency
ThetaIncremDeg = 2  # angle increments to test
ThetaIncremRad = ThetaIncremDeg * np.pi / 180  # radians
ThetaWidth = WidthofBeams * np.pi / 180
ThetaA = np.arange(-ThetaWidth, ThetaWidth + ThetaIncremRad, ThetaIncremRad)  # range of angles
NumAngles = len(ThetaA)
steering_vector = np.ones((M, NumAngles), dtype=complex)
Phi = [np.pi / 2, -np.pi / 2]  # angles of HackRFs relative to the perpendicular axis

# Prepare steering vector
for ii in range(NumAngles):
    for i in range(M):
        mua = 2 * np.pi * R * np.cos(ThetaA[ii] + Phi[i]) / Lamda
        steering_vector[i, ii] = np.exp(-1j * mua)

# MQTT Setup
broker = "192.168.1.100"  # Change this to your broker IP address
topic = "doa/angle"
client = paho.Client()
client.connect(broker)

# Function to process data and estimate DOA
def process_stream(stream1, stream2):
    Xf = np.zeros((M, K // 2), dtype=complex)  # FFT storage
    angle_over_time = []  # Store angle estimates over time

    # find index in FFT output that corresponds to frequency of data
    fi = np.arange(0, K // 2) * fs / (K / 2)
    fidx = np.argmin(np.abs(fi - fd))  # Find closest index to fd

    try:
        while True:
            # Read HackRF A IQ values
            A_1 = np.frombuffer(stream1.read(K), dtype=np.int8).reshape((K // 2, 2))
            A = A_1[:, 0] + 1j * A_1[:, 1]

            # Read HackRF C IQ values
            A_2 = np.frombuffer(stream2.read(K), dtype=np.int8).reshape((K // 2, 2))
            B = A_2[:, 0] + 1j * A_2[:, 1]

            Xf[0, :] = np.fft.fft(A, K // 2)  # FFT for HackRF A
            Xf[1, :] = np.fft.fft(B, K // 2)  # FFT for HackRF C

            Xs = Xf[:, fidx]  # complex value of FFT at frequency of interest

            # Calculate power for each angle
            P = np.zeros(NumAngles)
            Rxx = np.conj(Xs).T @ Xs  # covariance matrix
            for i in range(NumAngles):
                P[i] = np.conj(steering_vector[:, i]) @ Rxx @ steering_vector[:, i]

            # Find angle with max power
            max_idx = np.argmax(P)
            angle_guess = -60 + 2 * (max_idx - 1)
            angle_over_time.append(angle_guess)

            # Send the estimated angle to ESP32
            client.publish(topic, str(angle_guess))
            print(f"Estimated Angle: {angle_guess}")

    except KeyboardInterrupt:
        print("Streaming interrupted. Closing streams.")
        stream1.close()
        stream2.close()

# Command to start streaming data from HackRFs
# Replace `hackrf_transfer` with appropriate streaming commands or methods
cmd1 = ['hackrf_transfer', '-r', '-', '-f', str(CarrierFreq), '-s', str(fs)]
cmd2 = ['hackrf_transfer', '-r', '-', '-f', str(CarrierFreq), '-s', str(fs)]

# Start HackRF streams
proc1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
proc2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE)

# Process the streamed data
process_stream(proc1.stdout, proc2.stdout)
