import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import numpy as np

# Global variables for data storage
doa_data = []  # List to store direction of arrival estimates
max_samples = 100  # Maximum number of samples to display in the plot

# MQTT configuration
broker = "mqtt://10.12.14.63:1883"  # Public broker, replace with your own if necessary
topic = "sample/doa"  # Topic for DoA estimates

def main():
    live_plot_mqtt()

# The callback for when the client receives a CONNACK response from the server
def on_connect(client, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to the DoA estimates topic
    client.subscribe(topic)


# The callback for when a PUBLISH message is received from the server
def on_message(client, msg):
    global doa_data

    # Assuming the message payload contains the DoA estimate in degrees
    try:
        doa_estimate = float(msg.payload.decode())
        doa_data.append(doa_estimate)
        if len(doa_data) > max_samples:  # Keep the list size constant
            doa_data.pop(0)  # Remove the oldest data point to create a shifting effect
    except ValueError:
        print("Invalid DoA estimate received")


# Function to initialize the plot
def init_plot():
    plt.ion()  # Interactive mode on
    fig, ax = plt.subplots()
    ax.set_xlim(0, max_samples)  # x-axis for last 'max_samples' estimates
    ax.set_ylim(-180, 180)  # Assuming DoA is in the range -180 to 180 degrees
    ax.set_xlabel('Time (samples)')
    ax.set_ylabel('Direction of Arrival (degrees)')
    ax.set_title('Live Direction of Arrival Estimates')
    line, = ax.plot([], [], lw=2)
    return fig, ax, line


# Function to update the plot with new DoA data
def update_plot(fig, ax, line):
    line.set_xdata(np.arange(len(doa_data)))
    line.set_ydata(doa_data)
    ax.set_xlim(0, max_samples)  # Maintain the x-axis range of 100 samples
    ax.set_ylim(-180, 180)  # Keep y-axis range constant for DoA estimates
    fig.canvas.draw()
    fig.canvas.flush_events()


# Main function to handle live plotting
def live_plot_mqtt():
    global doa_data

    # Initialize MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to MQTT broker
    client.connect(broker, 1883, 60)

    # Initialize plot
    fig, ax, line = init_plot()

    # Start the MQTT loop in a separate thread
    client.loop_start()

    # Plot the data in real-time
    try:
        while True:
            update_plot(fig, ax, line)
            plt.pause(0.1)  # Small pause for real-time update
    except KeyboardInterrupt:
        print("Plotting stopped")
        client.loop_stop()


if __name__ == "__main__":
    live_plot_mqtt()
