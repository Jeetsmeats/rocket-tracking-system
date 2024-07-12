import numpy as np
from matplotlib import pyplot as plt
from multiprocessing import Process
import time
import os

hackrf_A_file = "./shell_files/76cf.raw"
hackrf_C_file = "./shell_files/07cf.raw"

# os.popen(start_command)
# os.popen(trigger_C_command)

# time.sleep(2)

# os.popen(trigger_A_command)

# time.sleep(10)

# opening the file in read mode
# hackrf_A = open(hackrf_A_file, "rb+")
# hackrf_C = open(hackrf_C_file, "rb+")

start = time.time()

n_bytes = 1600000
while True:
    
    # hackrf_A.flush()
    # hackrf_C.flush()
    
    hackrf_A_data = np.fromfile(hackrf_A_file, count=n_bytes, dtype="int8")
    hackrf_C_data = np.fromfile(hackrf_C_file, count=n_bytes, dtype="int8")
    
    print(hackrf_A_data)
    print(hackrf_C_data)
    
    # hackrf_A.truncate(0)
    # hackrf_C.truncate(0)
    
    # hackrf_A.write(('\0' * len(hackrf_A_data)).encode())
    # hackrf_C.write(('\0' * len(hackrf_C_data)).encode())
    
    # print(len(hackrf_A.read()))
    # print(len(hackrf_C.read()))
    
    # print(time.time() - start)
    # hackrf_A_data = np.array(hackrf_A_buffer).astype(np.int8)
    # hackrf_C_data = np.array(hackrf_C_buffer).astype(np.int8)
    
    time.sleep(0.5)
    
# plt.subplot(1, 2, 1)

# plt.plot(hackrf_A_data)
# plt.title("HackRF A Data")
# plt.xlim((0, 100))

# plt.subplot(1, 2, 2)

# plt.plot(hackrf_C_data, color="red")
# plt.title("HackRF C Data")
# plt.xlim((0, 100))

# plt.show()