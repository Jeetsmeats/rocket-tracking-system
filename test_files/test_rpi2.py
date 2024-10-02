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
    f = 915e6
    f_sample = 10e6
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
            freq = fftfreq(n, 1 / f_sample)

            # Desired Freq index
            index = np.argmin(np.abs(freq - f))

            # Real and Imaginary components of signal
            real = np.real(fft_signal[index])
            imag = np.imag(fft_signal[index])

            fft_dict["real"] = str(real)
            fft_dict["imag"] = str(imag)

            # Publishing Signal
            payload = orjson.dumps(fft_dict)

            # Lock processes
            with lock:
                client.publish(topic, payload)

            start_event.clear()
            next_event.set()

            time.sleep(0.01)

                
def on_connect(rc):

    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        Exception("Failed to connect, return code %d\n")


def main():
        
    topic = "test/topic"
    
    mqtt_id_3 = "f265020c6a9c"
    mqtt_id_4 = "ad13a4cc4122"
    
    pipe_C_path = "/home/Jeetsmeats/Documents/rocket-tracking-system/shell_files/pipes/hackrfC.pipe"
    pipe_D_path = "/home/Jeetsmeats/Documents/rocket-tracking-system/shell_files/pipes/hackrfD.pipe"
    
    mqtt_address = "10.12.14.63"

    lock = Lock()
    event_C = Event()
    event_D = Event()

    event_C.set()

    print("Starting HackRF D")
    process = Process(target=process_signal, args=(mqtt_id_3, topic, "board D", pipe_D_path , mqtt_address, lock, event_D, event_C))

    process.start()

    print("Starting HackRF C")
    process_signal(mqtt_id_4, topic, "board C", pipe_C_path , mqtt_address, lock, event_C, event_D)

if __name__ == "__main__":
    main()