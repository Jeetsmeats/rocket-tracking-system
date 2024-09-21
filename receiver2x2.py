import numpy as np
from numpy.fft import fft
from matplotlib import pyplot as plt
import paho.mqtt.client as paho
import subprocess
import os
import pyserial

# Constants
fs = 10 * 10**6  # sample rate
K = 4096 * 2  # number of samples real + imaginary per time step
fd = 1e6  # frequency of data
c = 3e8  # speed of light
M = 4  # number of arrays
R = 0.08  # half the distance between the two arrays
CarrierFreq = 915e6  # 915 MHz
WidthofBeams = 60  # width of the beams
Lamda = c / CarrierFreq  # wavelength of Signal frequency
ThetaIncremDeg = 2  # angle increments to test
ThetaIncremRad = ThetaIncremDeg * np.pi / 180  # radians
ThetaWidth = WidthofBeams * np.pi / 180
azimuthA = np.arange(-ThetaWidth, ThetaWidth + ThetaIncremRad, ThetaIncremRad) 
elevationA = np.arange(0, ThetaWidth + ThetaIncremRad, ThetaIncremRad)  
NumAzimuthAngles = len(azimuthA)
NumElevationAngles = len(elevationA)
NumAnglePairs = NumAzimuthAngles*NumElevationAngles
steering_vector = np.ones((M, NumAnglePairs), dtype=complex)
Phi = [np.pi/4, 3* np.pi / 4, 5* np.pi / 4, 7*np.pi/4]  # angles of HackRFs relative to the perpendicular axis

curr_azimuth_angle = 0
curr_elevation_angle = 0
idx = 0

# Prepare steering vector
for i in range(NumAzimuthAngles):
    for j in range(NumElevationAngles):
        curr_azimuth_angle = azimuthA[i]
        curr_elevation_angle = elevationA[j]
        idx = (i-1)*NumElevationAngles + j
        for k in range(M):
            mua = 2*np.pi*R*( np.cos(Phi[k])*np.cos(curr_azimuth_angle)*np.cos(curr_elevation_angle) + np.sin(Phi[k])*np.sin(curr_azimuth_angle)*np.cos(curr_elevation_angle) ) / (Lamda)
            steering_vector[k, idx] = np.exp(-1j*mua)


# MQTT Setup
broker = "192.168.1.100"  # Change this to your broker IP address
topic = "doa/angle"
client = paho.Client()
client.connect(broker)

ser = serial.Serial('dev/ttyS0', 9600, timeout=1)



# Function to process data and estimate DOA
def process_stream():
    Xf = np.zeros((M, K // 2), dtype=complex)  # FFT storage
    angle_over_time = []  # Store angle estimates over time
    estimated_azimuth = 0
    estimated_elevation = 0
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

            # Read HackRF C IQ values
            A_3 = np.frombuffer(stream3.read(K), dtype=np.int8).reshape((K // 2, 2))
            C = A_3[:, 0] + 1j * A_3[:, 1]

            # Read HackRF C IQ values
            A_4 = np.frombuffer(stream4.read(K), dtype=np.int8).reshape((K // 2, 2))
            D = A_4[:, 0] + 1j * A_4[:, 1]

            Xf[0, :] = np.fft.fft(A, K // 2)  # FFT for HackRF A
            Xf[1, :] = np.fft.fft(B, K // 2)  # FFT for HackRF C
            Xf[2, :] = np.fft.fft(C, K // 2)  # FFT for HackRF C
            Xf[3, :] = np.fft.fft(D, K // 2)  # FFT for HackRF C

            Xs = Xf[:, fidx]  # complex value of FFT at frequency of interest

            # Calculate power for each angle
            P = np.zeros(NumElevationAngles)
            Rxx = np.conj(Xs).T @ Xs  # covariance matrix
            for i in range(NumAnglePairs):
                P[i] = np.conj(steering_vector[:, i]) @ Rxx @ steering_vector[:, i]

            # Find angle with max power
            max_idx = np.argmax(P)
            estimated_azimuth = -60 + 5*np.floor((max_idx-1)/13)
            estimated_elevation = 5*np.mod(max_idx-1, 13)
            
            # Send the estimated angle to ESP32
            # client.publish(topic, str(angle_guess))
            print(f"Estimated Azimuth Angle: {estimated_azimuth}")
            print(f"Estimated Elevation Angle: {estimated_elevation}")
            # send to arduino.
            data_string = f"{estimated_elevation},{estimated_azimuth}\n"
            ser.write(data_string.encode())

    except KeyboardInterrupt:
        print("Streaming interrupted. Closing streams.")

def main():

    process_stream()