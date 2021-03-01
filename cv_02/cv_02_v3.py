# .py file for 2nd exercise
# Exercise 3: Fibonacci Sequence
from fei.ppds import Thread
from fei.ppds import Mutex
from fei.ppds import Semaphore
from fei.ppds import Event


class Shared:
    def __init__(self, n):
        self.N = n
        self.counter = 0
        self.fibonacci = [0, 1] + [0] * n
        self.threads = [0] * (n + 1)
        self.mutex = Mutex()
        self.event = Event()
        self.event.signal()
        for j in range(n + 1):
            self.threads[j] = Semaphore(0)
        self.threads[0].signal(1)

    def fnc_fibonacci_seq(self, pin):
        self.threads[pin].wait()
        self.fibonacci[pin + 2] = self.fibonacci[pin] + self.fibonacci[pin + 1]
        self.threads[pin + 1].signal()


def sequence(thread_id, obj):
    obj.fnc_fibonacci_seq(thread_id)


r = 10
threads = [0] * r
shared = Shared(r)
for i in range(r):
    t = Thread(sequence, i, shared)
    threads[i] = t

for t in threads:
    t.join()

print(shared.fibonacci)
