# .py file for 2nd exercise
# Exercise 3: Fibonacci Sequence
from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore
from fei.ppds import print


class SimpleBarrier:
    def __init__(self, n):
        self.N = n
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.N:
            self.counter = 0
            self.turnstile.signal(self.N)
        self.mutex.unlock()
        self.turnstile.wait()


def fnc_counter(arr, n):
    sleep(randint(1, 10)/10)
    tmp = arr[n] + arr[n - 1]
    return tmp


def rendezvous(thread_name):
    sleep(randint(1, 10) / 10)
    print('rendezvous: Thread %d' % thread_name)


def sequence(thread_id, barrier_1, barrier_2):
    rendezvous(thread_id)
    barrier_1.wait()
    # vykonaj výpočet a pridaj prvok do poľa
    # ...
    barrier_2.wait()


r = 10
threads = list()
sb_1 = SimpleBarrier(r)
sb_2 = SimpleBarrier(r)
for i in range(r):
    t = Thread(sequence, i, sb_1, sb_2)
    threads.append(t)

for t in threads:
    t.join()
