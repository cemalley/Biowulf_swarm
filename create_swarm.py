import numpy as np
import pandas as pd
import ipython as ip

samples = ['VJ3736_1_S16', 'VJ3736_2_S17', 'VJ3736_3_S18', 'VJ3736_4_S19', 'VJ3736_5_S20', 'VJ3736_6_S21']

for sample in samples:
    print(sample, file=open('output.txt', "a"))