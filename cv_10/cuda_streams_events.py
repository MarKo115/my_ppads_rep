from numba import cuda
import numpy as np
from time import perf_counter

num_arrays = 200
array_len = 1024**2


@cuda.jit
def kernel(array):
    thd = cuda.grid(1)
    num_iters = array.size / cuda.blockDim.x
    for j in range(num_iters):
        i = j * cuda.blockDim.x + thd
        for k in range(50):
            array[i] *= 2
            array[i] /= 2


data = []
data_gpu = []
gpu_out = []
streams = []
start_events = []
end_events = []

# generate random arrays.
for _ in range(num_arrays):
    streams.append(cuda.stream())
    start_events.append(cuda.event())
    end_events.append(cuda.event())
    data.append(np.random.randn(array_len).astype('float32'))

t_start = perf_counter()

# copy arrays to GPU.
for k in range(num_arrays):
    data_gpu.append(cuda.to_device(data[k], stream=streams[k]))

# process arrays.
for k in range(num_arrays):
    start_events[k].record(streams[k])
    kernel[1, 32, streams[k]](data_gpu[k])

for k in range(num_arrays):
    end_events[k].record(streams[k])

# copy arrays from GPU.
for k in range(num_arrays):
    gpu_out.append(data_gpu[k].copy_to_host(stream=streams[k]))

t_end = perf_counter()

for k in range(num_arrays):
    assert (np.allclose(gpu_out[k], data[k]))

kernel_times = []

for k in range(num_arrays):
    kernel_times.append(cuda.event_elapsed_time(start_events[k], end_events[k]))

print('Total time: %f' % (t_end - t_start))
print('Mean kernel duration (milliseconds): %f' % np.mean(kernel_times))
print('Mean kernel standard deviation (milliseconds): %f' % np.std(kernel_times))


