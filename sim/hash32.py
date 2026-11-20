"""CPython's float hash for a given hash width (pyhash.c _Py_HashDouble): 61 bits on 64-bit builds, 31 on 32-bit (Pyodide)."""
import math
def hash_double(v, bits):
    P = (1 << bits) - 1
    m, e = math.frexp(v)
    sign = 1
    if m < 0: sign, m = -1, -m
    x = 0
    while m:
        x = ((x << 28) & P) | x >> (bits - 28)
        m *= 268435456.0; e -= 28
        y = int(m); m -= y; x += y
        if x >= P: x -= P
    e = e % bits if e >= 0 else bits - 1 - ((-1 - e) % bits)
    x = ((x << e) & P) | x >> (bits - e)
    x *= sign
    return -2 if x == -1 else x
