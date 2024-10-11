import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import paho.mqtt.client as paho
import orjson
from scipy import constants
import time
from queue import Queue

Xs = np.complex64(np.zeros((1, 4)))

# Constants (unchanged from your original code)
fd = 915e6
c = constants.c
M = 4
R = (c / fd) / 2
beam_width = 60
w_length = c / fd
theta_increm_deg = 2
theta_increm_rad = theta_increm_deg * np.pi / 180
theta_width = beam_width * np.pi / 180
azimuth_A = np.arange(-theta_width, theta_width + theta_increm_rad, theta_increm_rad)
elevation_A = np.arange(0, theta_width + theta_increm_rad, theta_increm_rad)
n_azimuth_angles = len(azimuth_A)
n_elevation_angles = len(elevation_A)
n_angle_pair = n_azimuth_angles * n_elevation_angles
steering_vector = np.ones((M, n_angle_pair), dtype=complex)
phi = [np.pi/4, 3 * np.pi / 4, 5 * np.pi / 4, 7 * np.pi/4]

# Instantiate steering vector (unchanged)
for i in range(n_azimuth_angles):
    for j in range(n_elevation_angles):
        curr_azimuth_angle = azimuth_A[i]
        curr_elevation_angle = elevation_A[j]
        idx = (i-1)*n_elevation_angles + j
        for k in range(M):
            mua = 2 * np.pi * R * (np.cos(phi[k]) * np.cos(curr_azimuth_angle)*np.cos(curr_elevation_angle) +
                                   np.sin(phi[k])*np.sin(curr_azimuth_angle)*np.cos(curr_elevation_angle)) / (w_length)
            steering_vector[k, idx] = np.exp(-1j*mua)

steering_vector = np.array(steering_vector)

# Create a queue to share data between threads
angle_queue = Queue(maxsize=100)


plt.ion()
# Initialize the figure for real-time plotting
fig, ax = plt.subplots()
points = ax.scatter([], [], color='blue')  # Initialize empty scatter plot
ax.set_xlim(-90, 90)
ax.set_ylim(0, 90)
ax.set_xlabel('Azimuth (degrees)')
ax.set_ylabel('Elevation (degrees)')
ax.set_title('Real-Time Azimuth and Elevation')

# def update_plot(frame):
#
#     if not angle_queue.empty():
#
#         el, az = angle_queue.get()  # Retrieve the latest azimuth and elevation from the queue
#         sc.set_data(az, el)  # Update plot with new azimuth and elevation
#     return sc

# Modify the on_message function to include real-time plotting
def on_message(client, user_data, payload):
    decoded_json = orjson.loads(payload.payload.decode("utf-8"))
    imag = np.float64(decoded_json['imag'])
    real = np.float64(decoded_json['real'])
    board = decoded_json['Board']

    out = real + 1j * imag

    if user_data["count"] > 3:

        user_data["count"] = 0
        el, az = estimate_angle(Xs)
        angle_queue.put((el, az))
    else:
        Xs[0][user_data["count"]] = out
        user_data["count"] += 1

# Process stream (unchanged)
def process_stream():
    broker = "10.12.14.63"
    topic = "test/topic"
    port = 1883

    client_id = "v9Sy4w8GWpNv"
    client = paho.Client(client_id=client_id, protocol=paho.MQTTv5)
    client.connect(broker, port)

    client.subscribe(topic)

    user_data = {'count': 0, 'elevation': 0, 'azimuth': 0}
    client.user_data_set(user_data)

    client.on_message = on_message
    client.loop_start()

    while True:

        # Get azimuth and elevation from the queue
        el, az = angle_queue.get()
        print(el, az)

        # el = np.mod(el, 360)
        # az = np.mod(az, )
        #
        # if el < 90 and abs(az) <= 90:
        #     # Append new values to the lists
        #     data_el.insert(0, el)
        #     data_az.insert(0, az)
        #
        #     # Ensure that only the last 100 points are stored
        #     if len(data_el) > 100 or len(data_az) > 100:
        #         data_el.pop()
        #         data_az.pop()
        #
        #     # Update the scatter plot with the new data
        #     points.set_offsets(np.column_stack((data_az, data_el)))
        #     # points.set_xdata(data_az)
        #     # points.set_ydata(data_el)
        #
        #     plt.draw()
        #     plt.pause(0.01)
        # else:
        #     print(el, az)
def estimate_angle(Xs):
    P = np.zeros(n_angle_pair)
    Rxx = np.matmul(np.transpose(np.conj(Xs)), Xs)
    for i in range(n_angle_pair):
        P[i] = np.matmul(np.matmul(np.transpose(np.conj(steering_vector[:, i])), Rxx), steering_vector[:, i])

    max_idx = np.argmax(P)
    estimated_azimuth = -60 + 5 * np.floor((max_idx - 1) / 13)
    estimated_elevation = 5 * np.mod(max_idx - 1, 13)
    return estimated_elevation, estimated_azimuth

# Main function (unchanged)
def main():
    process_stream()

if __name__ == '__main__':
    main()
