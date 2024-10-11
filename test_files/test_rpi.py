
import numpy as np
from numpy.fft import fft, fftshift, fftfreq
from multiprocessing import Process, Lock, Event
import paho.mqtt.client as paho
import orjson
import time

def process_signal(id, topic, board, pipe_path, address, lock, start_event, next_event):
    
    # Set the broker address and mqtt port
    broker = address
    port = 1883

    # Connect to broker
    client = paho.Client(client_id=id, protocol=paho.MQTTv5)
    client.on_connect = on_connect
    client.connect(broker, port)

    # Constants
    f = 915000000
    f_sample = 2000000
    n = 1024

    fft_dict = {
        "Board": board,
        "real": "",
        "imag": "",
    }

    with open(pipe_path, 'rb') as pipe:

        while True:

            # Read raw data
            raw_data = bytearray(pipe.read(2 * 8 * 1024))
            data = np.array(raw_data).astype(np.int8).astype(np.float64).view(np.complex128)

            # FFT
            fft_signal = fft(data, n)
            # freq = fftfreq(n, 1 / f_sample)

            # # Desired Freq index
            # index = np.argmin(np.abs(freq - f))

            # Real and Imaginary components of signal
            real = np.real(fft_signal[0])
            imag = np.imag(fft_signal[0])

            fft_dict["real"] = str(real)
            fft_dict["imag"] = str(imag)

            # Publishing Signal
            payload = orjson.dumps(fft_dict)

            # Lock processes
            with lock:
                client.publish(topic, payload)

            start_event.clear()
            next_event.set()

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
    
    pipe_A_path = "/home/Jeetsmeats/Documents/rocket-tracking-system/shell_files/pipes/hackrfA.pipe"
    pipe_B_path = "/home/Jeetsmeats/Documents/rocket-tracking-system/shell_files/pipes/hackrfB.pipe"
  
    
    mqtt_address = "10.12.14.63"
    # mqtt_address = "192.168.1.142"

    lock = Lock()
    event_A = Event()
    event_B = Event()

    # Set event A as starting event
    event_A.set()

    print("Starting HackRF B")
    process = Process(target=process_signal, args=(mqtt_id_1, topic, "board B", pipe_B_path , mqtt_address, lock, event_B, event_A))

    process.start()
    
    print("Starting HackRF A")
    process_signal(mqtt_id_2, topic, "board A", pipe_A_path , mqtt_address, lock, event_A, event_B)

if __name__ == "__main__":
    main()
