
import numpy as np
from numpy.fft import fft, fftshift
from matplotlib import pyplot as plt
from multiprocessing import Process, Lock, Event
import paho.mqtt.client as paho
from paho import mqtt
import RPi.GPIO as GPIO
import random
import time
import subprocess

def process_signal(id, topic, board, pipe_path, address):
    
    # Set the broker address and mqtt port
    broker = address
    port = 1883
    
    # Connect to broker
    client = paho.Client(client_id=id, protocol=paho.MQTTv5)
    client.on_connect = on_connect
    client.connect(broker, port)

    f = 915000000

    with open(pipe_path, 'rb') as pipe:
        
        data = np.array([])
        
        while True:
            
            raw_data = bytearray(pipe.read(2*8*1024))
            data = np.array(raw_data).astype(np.int8).astype(np.float64).view(np.complex128)

            # FFT 
            fft_signal = fft(data, 1024)
            
            real = np.real(fft_signal[len(fft_signal) // 2])
            imag = np.imag(fft_signal[len(fft_signal) // 2])
         
            client.publish(topic, f"Board: {board} Real: {real}, Imag: {imag}")
            time.sleep(0.01)
            

def on_connect(rc):

    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        Exception("Failed to connect, return code %d\n")


def main():
    
    topic = "test/topic"
    
    mqtt_id_1 = "4083e8a8d0dc"
    mqtt_id_2 = "fe91eb8bc508"
    
    pipe_A_path = "/home/Jeetsmeats/Documents/rocket-tracking-system/shell_files/pipes/hackrfA.pipe"
    pipe_B_path = "/home/Jeetsmeats/Documents/rocket-tracking-system/shell_files/pipes/hackrfB.pipe"
  
    mqtt_address = "10.12.19.190"

    print("Starting HackRF B")
    process = Process(target=process_signal, args=(mqtt_id_1, topic, "board B", pipe_B_path , mqtt_address,))

    process.start()
    
    print("Starting HackRF A")
    process_signal(mqtt_id_2, topic, "board A", pipe_A_path , mqtt_address,)

if __name__ == "__main__":
    main()