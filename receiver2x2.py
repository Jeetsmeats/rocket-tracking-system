import numpy as np
from numpy.fft import fft
from matplotlib import pyplot as plt
import paho.mqtt.client as paho
import os
import pyserial
import orjson
from scipy import constants

def prepare_steering_vector():

    # Constants
    fd = 915e6                                                                                          # Carrier Frequency
    c = constants.c                                                                                     # Light speed
    M = 4                                                                                               # Array size
    R = (c / fd) / 2                                                                                    # Half the distance between the two arrays
    beam_width = 60                                         # Beam width
    w_length = c / fd                                       # Wavelength of Signal frequency
    theta_increm_deg = 2                                    # angle increments to test
    theta_increm_rad = theta_increm_deg * np.pi / 180       # Convert to Radians
    theta_width = beam_width * np.pi / 180
    azimuth_A = np.arange(-theta_width, theta_width + theta_increm_rad, theta_increm_rad)
    elevation_A = np.arange(0, theta_width + theta_increm_rad, theta_increm_rad)
    n_azimuth_angles = len(azimuth_A)
    n_elevation_angles = len(elevation_A)
    n_angle_pair = n_azimuth_angles*n_elevation_angles
    steering_vector = np.ones((M, n_angle_pair), dtype=complex)
    phi = [np.pi/4, 3* np.pi / 4, 5* np.pi / 4, 7*np.pi/4]  # angles of HackRFs relative to the perpendicular axis

    # Instantiate steering vector
    for i in range(n_azimuth_angles):
        for j in range(n_elevation_angles):
            curr_azimuth_angle = azimuth_A[i]
            curr_elevation_angle = elevation_A[j]
            idx = (i-1)*n_elevation_angles + j
            for k in range(M):
                mua = 2*np.pi*R*(np.cos(phi[k])*np.cos(curr_azimuth_angle)*np.cos(curr_elevation_angle) + np.sin(phi[k])*np.sin(curr_azimuth_angle)*np.cos(curr_elevation_angle) ) / (w_length)
                steering_vector[k, idx] = np.exp(-1j*mua)

# ser = serial.Serial('dev/ttyS0', 9600, timeout=1)

def on_message(client, userdata, payload):

        client.publish("sample/doa", payload)
        # print(orjson.loads(payload))
        # # Assuming the message payload contains the DoA estimate in degrees
        # try:
        #     doa_estimate = float(msg.payload.decode())
        #     doa_data.append(doa_estimate)
        #     if len(doa_data) > max_samples:  # Keep the list size constant
        #         doa_data.pop(0)  # Remove the oldest data point to create a shifting effect
        # except ValueError:
        #     print("Invalid DoA estimate received")


# Function to process data and estimate DOA
def process_stream():

    # MQTT Setup
    broker = "10.12.14.63"  # Change this to your broker IP address
    topic = "test/topic"
    client = paho.Client()
    client.connect(broker)

    client.subscribe(topic)
    client.loop_start()
    # try:
    #     while True:


            # # Calculate power for each angle
            # P = np.zeros(n_elevation_angles)
            # Rxx = np.conj(Xs).T @ Xs  # covariance matrix
            # for i in range(n_angle_pair):
            #     P[i] = np.conj(steering_vector[:, i]) @ Rxx @ steering_vector[:, i]
            #
            # # Find angle with max power
            # max_idx = np.argmax(P)
            # estimated_azimuth = -60 + 5*np.floor((max_idx-1)/13)
            # estimated_elevation = 5*np.mod(max_idx-1, 13)
            #
            # # Send the estimated angle to ESP32
            # # client.publish(topic, str(angle_guess))
            # print(f"Estimated Azimuth Angle: {estimated_azimuth}")
            # print(f"Estimated Elevation Angle: {estimated_elevation}")
            # # send to arduino.
            # data_string = f"{estimated_elevation},{estimated_azimuth}\n"
            # ser.write(data_string.encode())
    #
    # except KeyboardInterrupt:
    #     print("Streaming interrupted. Closing streams.")

def main():

    process_stream()