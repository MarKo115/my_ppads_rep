# .py file for 2nd exercise
# Exercise 2: Reusable Barrier
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


def rendezvous(thread_name):
    sleep(randint(1, 10) / 10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)


def barrier_example(thread_name, simple_b1, simple_b2):
    while True:
        rendezvous(thread_name)
        # ... sb1.wait
        simple_b1.wait()
        ko(thread_name)
        # ... sb2.wait
        simple_b2.wait()


threads = list()
sb_1 = SimpleBarrier(5)
sb_2 = SimpleBarrier(5)
for i in range(5):
    t = Thread(barrier_example, 'Thread %d' % i, sb_1, sb_2)
    threads.append(t)

for t in threads:
    t.join()
