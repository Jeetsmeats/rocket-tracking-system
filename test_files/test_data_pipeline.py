import numpy as np
from numpy.fft import fft, fftshift
from matplotlib import pyplot as plt
from multiprocessing import Process
import paho.mqtt.client as paho
from paho import mqtt
import random
import time

def gen_signal(id, topic, board):
    broker = "192.168.1.142"
    port = 1883

    client = paho.Client(client_id=id, protocol=paho.MQTTv5)
    client.on_connect = on_connect
    client.connect(broker, port)

    f = 100
    w = 2 * np.pi * f
    t = np.linspace(0, 1, 200)
    x = t * np.pi / 180

    while True:
        random_phase = random.uniform(0, np.pi / 2)

        sig = np.sin(w * x + random_phase)

        random_noise = np.random.normal(0, 1, len(t))

        noisy_signal = sig + random_noise

        fft_signal = fft(noisy_signal, 4096)
        fft_shifted = fftshift(fft_signal)
        phase = random_phase

        client.publish(topic, f'Phase value {random_phase} from {board}')

        time.sleep(1)

def on_connect(rc):

    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        Exception("Failed to connect, return code %d\n")


def main():
    topic = "test/topic1"

    process1 = Process(target=gen_signal, args=("4083e8a8d0dc", topic, "board A"))
    process2 = Process(target=gen_signal, args=("fe91eb8bc508", topic, "board B"))
    process3 = Process(target=gen_signal, args=("f265020c6a9c", topic, "board C"))

    process1.start()
    process2.start()
    process3.start()

    gen_signal("ad13a4cc4122", topic, "board D")

if __name__ == "__main__":
    main()
