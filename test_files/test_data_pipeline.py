import numpy as np
from numpy.fft import fft, fftshift
from matplotlib import pyplot as plt
from multiprocessing import Process
import paho.mqtt.client as paho
from paho import mqtt
import random


def gen_signal(topic, board):
    broker = "192.168.1.142"
    port = 1883

    client = paho.Client(client_id="", protocol=paho.MQTTv5)
    client.on_connect = on_connect
    client.connect(broker, port)

    f = 915000000
    w = 2 * np.pi * f
    t = np.arange(0, 100000, 1)
    x = t * np.pi / 180

    while True:
        random_phase = random.uniform(0, np.pi / 2)

        sig = np.sin(w * x + random_phase)

        random_noise = np.random.normal(0, 5, len(t))

        noisy_signal = sig + random_noise

        fft_signal = fft(noisy_signal)
        desired_freq = fft_signal[0]

        phase = np.arctan2(np.imag(desired_freq), np.real(desired_freq))

        client.publish(topic, f'Phase value {phase} from {board}')


def on_connect(rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        Exception("Failed to connect, return code %d\n")


def main():
    topic = "topic/test1"

    process1 = Process(target=gen_signal, args=(topic, "board A"))
    process2 = Process(target=gen_signal, args=(topic, "board B"))
    process3 = Process(target=gen_signal, args=(topic, "board C"))

    process1.start()
    process2.start()
    process3.start()


if __name__ == "__main__":
    main()
