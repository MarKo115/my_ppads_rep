# .py file for 1st project
from fei.ppds import Thread
from fei.ppds import Mutex
from collections import Counter


class Shared():
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.elms = [0] * self.end
        self.mutex = Mutex()


def fnc_counter(shared):
    while True:
        if shared.counter >= shared.end:
            return
        shared.elms[shared.counter] += 1
        shared.mutex.lock()
        shared.counter += 1
        shared.mutex.unlock()


for i in range(10):
    sh = Shared(1_000_000)
    t1 = Thread(fnc_counter, sh)
    t2 = Thread(fnc_counter, sh)

    t1.join()
    t2.join()

    print(Counter(sh.elms))
