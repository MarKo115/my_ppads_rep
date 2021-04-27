import numpy
from numba import cuda


@cuda.jit
def my_kernel2(io_array):
    pos = cuda.grid(1)
    if pos < io_array.size:
        io_array[pos] *= 2


@cuda.jit
def my_kernel(io_array):
    """
    code for kernel
    """
    # Thread id in a 1D block
    tx = cuda.threadIdx.x
    # Block id in a 1D grid
    ty = cuda.blockIdx.x
    # Block width, number of thread per block
    bw = cuda.blockDim.x
    # Compute index inside the array
    pos = bw * ty + tx
    # Check array boundaries
    if pos < io_array.size:
        # do the computation
        io_array[pos] *= 2


data = numpy.ones(256)
threads_per_block = 32
blocks_per_grid = (data.size + (threads_per_block-1))//threads_per_block
my_kernel[blocks_per_grid, threads_per_block](data)
print(data)
