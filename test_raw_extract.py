import numpy as np
from matplotlib import pyplot as plt
from multiprocessing import Process
import time
import subprocess
from multiprocessing import Process, Queue

start = time.time()

def read_pipe(pipe_path, q):
    
    with open(pipe_path, 'rb') as pipe:
        
        start_time = time.time()
        data = np.array([])
        
        while time.time() - start_time < 10:
            
            raw_data = bytearray(pipe.read(8*1024))
            data = np.append(data, np.array(raw_data).astype(np.int8))
    
        q.put(data)
                        
def start_pipeline():
    
    start_clk = ['hackrf_clock', '-o', '1', '-d', '0000000000000000675c62dc302745cf']
    
    commands = {'HackRF A': ['hackrf_transfer', '-d', '0000000000000000675c62dc335c76cf', '-a', '0', '-f', '915000000', '-s', '10000000', '-r', 'shell_files/pipes/hackrfA.pipe'],
                'HackRF B': ['hackrf_transfer', '-d', '0000000000000000675c62dc302745cf', '-a', '0', '-f', '915000000', '-s', '10000000', '-r', 'shell_files/pipes/hackrfA.pipe'],
                'HackRF C': ['hackrf_transfer', '-H', '-d', '0000000000000000675c62dc304807cf', '-a', '0', '-f', '915000000', '-s', '10000000', '-r', 'shell_files/pipes/hackrfC.pipe'],
                'HackRF D': ['hackrf_transfer', '-d', '0000000000000000675c62dc304807cf', '-a', '0', '-f', '915000000', '-s', '10000000', '-r', 'shell_files/pipes/hackrfA.pipe'],
                }
    
    task1 = subprocess.run(start_clk)
    # subprocess.run(commands['HackRF C'], shell=True)
    task2 = subprocess.run(commands['HackRF A'])
        
def main():
    'HackRF A',
    q1 = Queue()
    q2 = Queue()
    process1 = Process(target=read_pipe, args=('./shell_files/pipes/hackrfC.pipe', q1, ))
    process2 = Process(target=read_pipe, args=('./shell_files/pipes/hackrfA.pipe', q2, ))
    
    process1.start()
    time.sleep(2)
    process2.start()
    
    start_time = time.time()
    # for i in range(10):
        
    #     t_start = time.time()
    #     t = 0
        
    #     while t < 5:
    #         t = time.time() - t_start
        
    #     print(f'Time Elapsed: {time.time() - start_time}')


    if time.time() - start_time > 13:
        process1.join()
        process2.join()
    
    data_C = q1.get()
    data_A = q2.get()
    
    print(f'Data from HackRF A: {data_A}')
    print(f'Data from HackRF C: {data_C}')
    
    data_C_I = data_C[0::2]
    data_C_Q = data_C[1::2]
    
    data_A_I = data_A[0::2]
    data_A_Q = data_A[1::2]
    plt.subplot(1, 2, 1)
    plt.plot(data_C_I[:100000], label="In-Phase")
    plt.plot(data_C_Q[:100000], label="Quadrature")
    plt.xlabel("N (Datapoints)")
    plt.ylabel("Magnitude")
    plt.title("HackRF C Data")
    
    plt.subplot(1, 2, 2)
    plt.plot(data_A_I[:100000], label="In-Phase")
    plt.plot(data_A_Q[:100000], label="Quadrature")
    plt.xlabel("N (Datapoints)")
    plt.ylabel("Magnitude")
    plt.title("HackRF A Data")
    
    plt.show()
main()