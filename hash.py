# -*- coding: utf-8 -*-
"""
@author: David Candela Rubio and Guillermo Raya García
"""

import hashlib
from typing import Optional, Tuple

def uab_md5(message: str, num_bits: int) -> Optional[int]:
    try:
        assert(0 < num_bits <= 128)
        num_shift =  8 - num_bits % 8
        num_bytes = num_bits // 8 + 1
        h = hashlib.md5(str.encode(message)).digest()
        num = int.from_bytes(h[:num_bytes], byteorder='big')
        num = num >> num_shift
        return num
    except:
        return None

def second_preimage(message: str, num_bits : int) -> Optional[Tuple[str, int]]:
    pass

def collision(num_bits: int) -> Optional[Tuple[str, str, int]]:
    pass

