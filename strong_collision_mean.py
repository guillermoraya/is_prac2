# -*- coding: utf-8 -*-
"""
@author: david
"""

import numpy as np
import matplotlib.pyplot as plt

# Tan simple que se puede hacer en tan solo una línea de còdigo
def sm(b): 1 + np.sum(np.cumprod(np.arange(1 << b, 0, -1) / (1 << b)))

def strong_mean(bits):
    size = 1 << bits
    descending = np.arange(size, 0, -1, dtype=np.float64) / size
    probability = np.cumprod(descending)
    return np.sum(probability) + 1

bit_range = np.arange(24) + 1
mean_range = list(map(strong_mean, bit_range))

plt.plot(bit_range, mean_range,
         c='red', linestyle='-.', label='Mitjana')
plt.title("Col·lisions fortes")
plt.ylabel("Nombre de iteracions")
plt.xlabel("Nombre de bits")
plt.yscale("log")
plt.legend()
plt.show()