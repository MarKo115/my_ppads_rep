# .py file for 2nd exercise
# Exercise 1: ADT SimpleBarrier
from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex
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


def barrier_example(barrier, thread_id):
    sleep(randint(1, 10) / 10)
    print("vlakno %s pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %s po bariere" % thread_id)


sb = SimpleBarrier(5)
for i in range(5):
    t = Thread(barrier_example, sb, f'Thread {i}')
