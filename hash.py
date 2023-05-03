# -*- coding: utf-8 -*-
"""
@author: David Candela Rubio and Guillermo Raya García
"""

import math
import string
import random
import hashlib
from time import perf_counter as get_time
from typing import Optional, Tuple, Callable, Iterable, Any

MAX_ITER = int(1e8)
ASCII = string.ascii_uppercase + string.ascii_lowercase + string.digits


def random_string(N: int = 7) -> str:
    """
    Generate a random string of size N (default 7) with ASCII alphanumerics
    """
    return ''.join(random.choices(ASCII, k=N))


def uab_md5(message: str, num_bits: int) -> Optional[int]:
    try:
        assert(0 < num_bits <= 128)
        num_shift = -num_bits % 8
        num_bytes = math.ceil(num_bits / 8)
        h = hashlib.md5(str.encode(message)).digest()
        num = int.from_bytes(h[:num_bytes], byteorder='big')
        num = num >> num_shift
        return num
    except:
        return None


def second_preimage(message: str, num_bits: int) -> Optional[Tuple[str, int]]:
    out = None
    h = uab_md5(message, num_bits)
    hm = h
    if h is None:
        return
    m = '-' if message[0] == '+' else '+'
    for i in range(MAX_ITER):
        res = random_string(num_bits)
        h_prime = uab_md5(m + res, num_bits)
        hm = max(hm, h_prime)
        if h == h_prime:
            out = (m + res, i)
            break
    return out


def collision(num_bits: int) -> Optional[Tuple[str, str, int]]:
    hashDictionary = {}
    foundCollision = False
    iterationCounter = 0
    while not foundCollision:
        iterationCounter += 1
        newString = random_string(num_bits)
        key = uab_md5(newString, num_bits)
        collision = hashDictionary.get(key, None)
        if collision is None:
            hashDictionary[key] = newString
        else:
            foundCollision = (newString != collision)
    return (collision, newString, iterationCounter)


def measure(function: Callable, value_range: Iterable[Any],
            value_name: Optional[str] = None, repeats: int = 10,
            **func_args: Any
            ) -> Tuple[Iterable[Iterable[Any]], Iterable[Iterable[Any]]]:
    results_value = []
    results_time = []
    if value_name is not None:
        call = lambda value: function(**{value_name: value}, **func_args)
    else:
        call = lambda value: function(value, **func_args)
    for value in value_range:
        result_value = []
        result_time = []
        for _ in range(repeats):
            time = get_time()
            result_value.append(call(value))
            result_time.append(get_time() - time)
        results_value.append(result_value)
        results_time.append(result_time)
    return results_value, results_time


def arg_at(args: Optional[Tuple[Any]], index: int) -> Optional[Any]:
    if args is None or not (0 <= index < len(args)):
        return None
    return args[index]


def _main():
    bit_range = np.arange(24) + 1

    # COLISIONS FORTES
    collisions, time = measure(collision, bit_range, repeats=50)
    collisions = np.array([[arg_at(repeat, 2)
                          for repeat in bit_size] for bit_size in collisions])
    time = np.array(time)

    info = pd.DataFrame(collisions.T, columns=bit_range)

    timing = pd.DataFrame(time.T, columns=bit_range)
    info.describe().transpose()[["25%", "mean", "75%"]].plot()
    plt.ylabel("Iteracions")
    plt.xlabel("Nombre de bits")
    plt.yscale("log")
    plt.show()

    timing.describe().transpose()[["25%", "mean", "75%"]].plot()
    plt.ylabel("Temps d'execució")
    plt.xlabel("Nombre de bits")
    plt.yscale("log")
    plt.show()

    # COLISIONS DEBILS
    collisions, time = measure(
        second_preimage, bit_range, repeats=5, value_name="num_bits", message=random_string())
    collisions = np.array([[arg_at(repeat, 1)
                          for repeat in bit_size] for bit_size in collisions])
    time = np.array(time)

    info = pd.DataFrame(collisions.T, columns=bit_range)

    timing = pd.DataFrame(time.T, columns=bit_range)
    info.describe().transpose()[["25%", "mean", "75%"]].plot()
    plt.ylabel("Iteracions")
    plt.xlabel("Nombre de bits")
    plt.yscale("log")
    plt.show()

    timing.describe().transpose()[["25%", "mean", "75%"]].plot()
    plt.ylabel("Temps d'execució")
    plt.xlabel("Nombre de bits")
    plt.yscale("log")
    plt.show()


if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt

    _main()
