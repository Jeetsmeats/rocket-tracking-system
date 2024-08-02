import numpy as np
from numpy.fft import fft, fftshift
from matplotlib import pyplot as plt
from multiprocessing import Process
import paho.mqtt.client as paho
from paho import mqtt
import random
import time
import subprocess

def process_signal(id, topic, board, pipe_path, address):
    broker = address
    port = 1883

    client = paho.Client(client_id=id, protocol=paho.MQTTv5)
    client.on_connect = on_connect
    client.connect(broker, port)

    f = 915000000

    with open(pipe_path, 'rb') as pipe:
        
        data = np.array([])
        
        while True:
            
            raw_data = bytearray(pipe.read(8*1024))
            data = np.append(data, np.array(raw_data).astype(np.int8).astype(np.float64).view(np.complex128))

            if len(data) > 100000:
                
                I = data[0::2]
                Q = data[1::2]
                
                
                fft_signal = fft(data, 1024)
                
                real = np.real(fft_signal[len(fft_signal) // 2])
                imag = np.imag(fft_signal[len(fft_signal) // 2])

                client.publish(topic, f"Board: {board} Real: {real}, Imag: {imag}")
                
                data = np.array([])
                time.sleep(0.05)
                

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
    
    mqtt_address = "10.12.23.21"

    # process1 = Process(target=process_signal, args=(mqtt_id_1, topic, "board D", pipe_D_path , mqtt_address))
    # process2 = Process(target=process_signal, args=(mqtt_id_2, topic, "board C", pipe_C_path , mqtt_address))
    process3 = Process(target=process_signal, args=(mqtt_id_3, topic, "board B", pipe_B_path , mqtt_address))

    # print("Starting HackRF D")
    # process1.start()
    # time.sleep(1)
    
    # print("Starting HackRF C")
    # process2.start()
    # time.sleep(1)
    
    print("Starting HackRF B")
    process3.start()
    
    print("Starting HackRF A")
    process_signal(mqtt_id_4, topic, "board A", pipe_A_path , mqtt_address)

if __name__ == "__main__":
    main()
