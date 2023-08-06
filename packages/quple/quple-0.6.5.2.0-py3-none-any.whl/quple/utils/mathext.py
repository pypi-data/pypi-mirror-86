from enum import Enum
import numba

class DataPrecision(Enum):
    single = 1
    double = 2

@numba.vectorize([numba.float64(numba.complex128),numba.float32(numba.complex64)])
def abs2(x):
    return x.real**2 + x.imag**2