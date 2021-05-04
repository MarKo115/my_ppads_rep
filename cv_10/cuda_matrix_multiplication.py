from numba import cuda
import numpy
import math
from time import perf_counter


# CUDA kernel
@cuda.jit
def matmul(A, B, C):
    """Perform matrix multiplication of C = A * B
    """
    row, col = cuda.grid(2)
    if row < C.shape[0] and col < C.shape[1]:
        tmp = 0.
        for k in range(A.shape[1]):
            tmp += A[row, k] * B[k, col]
        C[row, col] = tmp


data_A = []
data_B = []
streams = []
start_events = []
end_events = []
num_arrays = 100
A_gpu = []
B_gpu = []
C_gpu = []
C_out = []

# Host code
for _ in range(num_arrays):
    streams.append(cuda.stream())
    start_events.append(cuda.event())
    end_events.append(cuda.event())
    # Initialize the data arrays
    A = numpy.full((24, 12), 3, numpy.float64)  # matrix containing all 3's
    B = numpy.full((12, 22), 4, numpy.float64)  # matrix containing all 4's
    data_A.append(A)
    data_B.append(B)

t_start = perf_counter()

for i in range(num_arrays):
    # Copy the arrays to GPU
    A_gpu.append(cuda.to_device(data_A[i], stream=streams[i]))
    B_gpu.append(cuda.to_device(data_B[i], stream=streams[i]))

    # Allocate memory on the device for the result
    C_gpu.append(cuda.device_array((24, 22), stream=streams[i]))

for i in range(num_arrays):
    # Configure the blocks
    threadsperblock = (16, 16)
    blockspergrid_x = int(math.ceil(A.shape[0] / threadsperblock[0]))
    blockspergrid_y = int(math.ceil(B.shape[1] / threadsperblock[1]))
    blockspergrid = (blockspergrid_x, blockspergrid_y)

    # Start the kernel
    start_events[i].record(streams[i])
    matmul[blockspergrid, threadsperblock, streams[i]](A_gpu[i], B_gpu[i], C_gpu[i])

for i in range(num_arrays):
    end_events[i].record(streams[i])

for i in range(num_arrays):
    # Copy the result back to the host
    C_out.append(C_gpu[i].copy_to_host(stream=streams[i]))

t_end = perf_counter()
kernel_times = []

for i in range(num_arrays):
    kernel_times.append(cuda.event_elapsed_time(start_events[i], end_events[i]))

print('Total time: %f' % (t_end - t_start))
print('Mean kernel duration (milliseconds): %f' % numpy.mean(kernel_times))
print('Mean kernel standard deviation (milliseconds): %f' % numpy.std(kernel_times))


