from fei.ppds import Thread, Semaphore, Mutex, print
from time import sleep
from random import randint


class SimpleBarrier:
    def __init__(self, n):
        self.N = n
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)

    def wait(self, each=None, last=None):
        self.mutex.lock()
        self.counter += 1
        if each:
            print(each)
        if self.counter == self.N:
            self.counter = 0
            if last:
                print(last)
            self.turnstile.signal(self.N)
        self.mutex.unlock()
        self.turnstile.wait()


class SharedObject:
    def __init__(self, n):
        self.mutex = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(n)
        self.barrier2 = SimpleBarrier(n)


def get_serving_from_pot(shared, savage_id):
    print("Savage %2d: taking a portion" % savage_id)
    shared.servings -= 1


def put_serving_in_pot(m, shared):
    print("Chef: cooking")
    sleep(0.4 + randint(0, 2) / 10)
    shared.servings += m


def cook(m, shared):
    while True:
        shared.empty_pot.wait()
        put_serving_in_pot(m, shared)
        shared.full_pot.signal()


def eat(savage_id):
    print("Savage %2d: eating" % savage_id)
    sleep(0.2 + randint(0, 3) / 10)


def savage(savage_id, shared):
    while True:
        shared.barrier2.wait(each=f"Savage {savage_id}: come for dinner",
                             last=f"Savage {savage_id}: you can start eat")
        shared.mutex.lock()
        if shared.servings == 0:
            shared.empty_pot.signal()
            shared.full_pot.wait()
        get_serving_from_pot(shared, savage_id)
        shared.mutex.unlock()
        eat(savage_id)
        shared.barrier1.wait(last="\n")


def run_model(n, m):
    threads = list()
    shared = SharedObject(n)
    for savage_id in range(n):
        threads.append(Thread(savage, savage_id, shared))
    threads.append(Thread(cook, m, shared))

    for t in threads:
        t.join()


if __name__ == "__main__":
    N = 3
    M = 3
    run_model(N, M)
