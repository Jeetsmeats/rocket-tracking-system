import numpy as np
from matplotlib import pyplot as plt
from multiprocessing import Process
from time import time
import subprocess

start = time()

trigger_A = ['hackrf_transfer', '-d', '0000000000000000675c62dc335c76cf', '-a', '0', '-f', '915000000', '-s', '20000000', '-r', './pipes/hackrfA_pipe']
hackrf_A_stream = subprocess.Popen(trigger_A, stdout=subprocess.PIPE)

for iq_samples in iter(lambda: bytearray(hackrf_A_stream.read(8 * 1024)), b''):
        # convert the samples chunk for use by numpy, if you wish
        data = np.array(iq_samples)
        print(data)