from __future__ import division
from numba import cuda
import numpy
import math


# CUDA kernel
@cuda.jit
def my_fibonacci(io_array, start):
    pos = cuda.grid(1)
    index = pos + start
    if pos < io_array.size:
        # do the computation
        io_array[index] = io_array[start - 2] + io_array[start - 1]


# Host code
data = numpy.ones(256)
data[0] = 0
data[3] = 2
threadsperblock = 256
blockspergrid = math.ceil(data.shape[0] / threadsperblock)
s = 4
n = 256

while s <= 16:
    my_fibonacci[blockspergrid, threadsperblock](data, s)
    s += 1

print(data)


