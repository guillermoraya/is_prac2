# -*- coding: utf-8 -*-
"""
@author: David Candela Rubio and Guillermo Raya García
"""

import string
import random
import hashlib
from time import perf_counter as get_time
from typing import Optional, Tuple, Callable, Iterable, Any

ASCII = string.ascii_uppercase + string.ascii_lowercase + string.digits


def random_string(N: int = 7) -> str:
    """
    Generate a random string of size N (default 7) with ASCII alphanumerics
    """
    return ''.join(random.choices(ASCII, k=N))


def uab_md5(message: str, num_bits: int) -> Optional[int]:
    try:
        assert(0 < num_bits <= 128)
        h = hashlib.md5(str.encode(message)).digest()
        num = int.from_bytes(h, byteorder='big')
        num = num >> (128 - num_bits)
        return num
    except:
        return None


def second_preimage(message: str, num_bits: int) -> Optional[Tuple[str, int]]:
    h = uab_md5(message, num_bits)
    hm = h
    if h is None:
        return
    m = '-' if message[0] == '+' else '+'
    foundPreimage = False
    iterationCounter = 0
    while not foundPreimage:
        iterationCounter += 1
        res = random_string(num_bits)
        h_prime = uab_md5(m + res, num_bits)
        hm = max(hm, h_prime)
        if h == h_prime:
            foundPreimage = True
    return (m + res, iterationCounter)


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
        def call(value): return function(**{value_name: value}, **func_args)
    else:
        def call(value): return function(value, **func_args)
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
    bit_name = list(
        map(lambda n: str(n) + f" bit{'' if n == 1 else 's'}", bit_range))
    repeats = 20
    info = pd.DataFrame(index=bit_name)


    # COL·LISIONS FORTES
    collisions, time = measure(collision, bit_range, repeats=repeats)
    collisions = np.array([[arg_at(repeat, 2)
                          for repeat in bit_size] for bit_size in collisions])
    time = np.array(time)

    mu = collisions.mean(axis=-1)
    sigma = collisions.std(axis=-1, ddof=1) / np.sqrt(repeats)
    info["Iterations mean"] = list(map("{:8.1f}".format, mu))
    info["Iterations error"] = list(map("{:8.2f}".format, sigma))
    plt.fill(list(bit_range) + list(bit_range)[::-1],
             list(mu + 1.96 * sigma) + list(mu - 1.96 * sigma)[::-1],
             c='blue', alpha=0.5, label='CI del 95% per la mitjana')
    plt.plot(bit_range, mu, c='red', linestyle='-.', label='Mitjana')
    plt.title("Col·lisions fortes")
    plt.ylabel("Nombre de iteracions")
    plt.xlabel("Nombre de bits")
    plt.yscale("log")
    plt.legend()
    plt.show()
    
    mu = time.mean(axis=-1)
    sigma = time.std(axis=-1, ddof=1) / np.sqrt(repeats)
    info["Execution mean"] = list(map("{:8.3f}".format, 1e3 * mu))
    info["Execution error"] = list(map("{:8.4f}".format, 1e3 * sigma))
    plt.fill(list(bit_range) + list(bit_range)[::-1],
             list(mu + 1.96 * sigma) + list(mu - 1.96 * sigma)[::-1],
             c='blue', alpha=0.5, label='CI del 95% per la mitjana')
    plt.plot(bit_range, mu, c='red', linestyle='-.', label='Mitjana')
    plt.title("Col·lisions fortes")
    plt.ylabel("Temps d'execució (s)")
    plt.xlabel("Nombre de bits")
    plt.yscale("log")
    plt.legend()
    plt.show()

    with open("strong_collision - tables.txt", 'w') as handler:
        handler.write(info.style.to_latex())
        
    # COL·LISIONS DEBILS
    collisions, time = measure(
        second_preimage, bit_range, repeats=repeats, value_name="num_bits", message=random_string())
    collisions = np.array([[arg_at(repeat, 1)
                          for repeat in bit_size] for bit_size in collisions])
    time = np.array(time)

    mu = collisions.mean(axis=-1)
    sigma = collisions.std(axis=-1, ddof=1) / np.sqrt(repeats)
    info["Iterations mean"] = list(map("{:10.1f}".format, mu))
    info["Iterations error"] = list(map("{:10.2f}".format, sigma))
    plt.fill(list(bit_range) + list(bit_range)[::-1],
             list(mu + 1.96 * sigma) + list(mu - 1.96 * sigma)[::-1],
             c='blue', alpha=0.5, label='CI del 95% per la mitjana')
    plt.plot(bit_range, mu, c='red', linestyle='-.', label='Mitjana')
    plt.title("Col·lisions dèbils")
    plt.ylabel("Nombre de iteracions")
    plt.xlabel("Nombre de bits")
    plt.yscale("log")
    plt.legend()
    plt.show()

    mu = time.mean(axis=-1)
    sigma = time.std(axis=-1, ddof=1) / np.sqrt(repeats)
    info["Execution mean"] = list(map("{:10.3f}".format, 1e3 * mu))
    info["Execution error"] = list(map("{:10.4f}".format, 1e3 * sigma))
    plt.fill(list(bit_range) + list(bit_range)[::-1],
             list(mu + 1.96 * sigma) + list(mu - 1.96 * sigma)[::-1],
             c='blue', alpha=0.5, label='CI del 95% per la mitjana')
    plt.plot(bit_range, mu, c='red', linestyle='-.', label='Mitjana')
    plt.title("Col·lisions dèbils")
    plt.ylabel("Temps d'execució (s)")
    plt.xlabel("Nombre de bits")
    plt.yscale("log")
    plt.legend()
    plt.show()

    with open("weak_collision - tables.txt", 'w') as handler:
        handler.write(info.style.to_latex())
        

if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt

    _main()
