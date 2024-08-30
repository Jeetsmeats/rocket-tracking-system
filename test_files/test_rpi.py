
import numpy as np
from numpy.fft import fft, fftshift
from matplotlib import pyplot as plt
from multiprocessing import Process
import paho.mqtt.client as paho
from paho import mqtt
import RPi.GPIO as GPIO
import random
import time
import subprocess

def process_signal(id, topic, board, pipe_path, address, run_pin):
    
    # Set the synchronisation testing pin
    test_pin = 12
    
    if run_pin:
        # Set up GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(test_pin, GPIO.OUT)
    
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
                
            # I = data[0::2]
            # Q = data[1::2]
            
            if run_pin:
                GPIO.output(test_pin, GPIO.HIGH)
                
            # FFT Test Pulse
            fft_signal = fft(data, 1024)
            
            if run_pin:
                GPIO.output(test_pin, GPIO.LOW)
            
            real = np.real(fft_signal[len(fft_signal) // 2])
            imag = np.imag(fft_signal[len(fft_signal) // 2])

            client.publish(topic, f"Board: {board} Real: {real}, Imag: {imag}")
            
            data = np.array([])
                

def on_connect(rc):

    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        Exception("Failed to connect, return code %d\n")


def main():
    
    topic = "test/topic"
    
    mqtt_id_1 = "4083e8a8d0dc"
    mqtt_id_2 = "fe91eb8bc508"
    mqtt_id_3 = "f265020c6a9c"
    mqtt_id_4 = "ad13a4cc4122"
    
    pipe_A_path = "./shell_files/pipes/hackrfA.pipe"
    pipe_B_path = "./shell_files/pipes/hackrfB.pipe"
    pipe_C_path = "./shell_files/pipes/hackrfC.pipe"
    pipe_D_path = "./shell_files/pipes/hackrfD.pipe"
    
    mqtt_address = "10.12.19.190"

    print("Starting HackRF D")
    process = Process(target=process_signal, args=(mqtt_id_1, topic, "board D", pipe_D_path , mqtt_address, True))

    print("Starting HackRF C")
    process_signal(mqtt_id_2, topic, "board C", pipe_C_path , mqtt_address, False)

if __name__ == "__main__":
    main()