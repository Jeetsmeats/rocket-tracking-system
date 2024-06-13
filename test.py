from pyhackrf2 import HackRF
import numpy as np
import math
from time import sleep

def pipe(data: bytes) -> bool:
    a = np.array(data).astype(np.int8)
    # print(f"a: {a}")
    print(a.shape)
    return False    # pipe function may return True to stop rx immediately


hackrf = HackRF()

hackrf.sample_rate = 20e6
hackrf.center_freq = 912e6

hackrf.sample_count_limit = 2 * 10 ** 6
hackrf.start_rx(pipe_function=pipe)
sleep(0.1)
hackrf.stop_rx()
