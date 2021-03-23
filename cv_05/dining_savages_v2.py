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
    def __init__(self, n, c):
        self.mutex = Mutex()
        self.chef_mutex = Mutex()
        self.servings = 0
        self.num_of_chefs = c
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(n)
        self.barrier2 = SimpleBarrier(n)
        self.chef_barrier2 = SimpleBarrier(c)
        self.chef_barrier = SimpleBarrier(c + 1)

    def wakeup(self):
        print("Hey chefs, wake up")
        self.chef_barrier.wait()


def get_serving_from_pot(shared, savage_id):
    print("Savage %2d: taking a portion" % savage_id)
    shared.servings -= 1


def put_serving_in_pot(m, shared, chef_id):
    print(f"Chef {chef_id}: cooking")
    sleep(0.4 + randint(0, 2) / 10)
    shared.servings += m


def eat(savage_id):
    print("Savage %2d: eating" % savage_id)
    sleep(0.2 + randint(0, 3) / 10)


def cook(shared, m, chef_id):
    shared.chef_mutex.lock()
    put_serving_in_pot(m, shared, chef_id)
    shared.full_pot.signal()
    shared.chef_mutex.unlock()


def savage(savage_id, shared):
    while True:
        shared.barrier2.wait(each=f"Savage {savage_id}: come for dinner",
                             last=f"Savage {savage_id}: you can start eat")
        shared.mutex.lock()
        if shared.servings == 0:
            shared.wakeup()
            shared.empty_pot.signal()
            shared.full_pot.wait()
        get_serving_from_pot(shared, savage_id)
        shared.mutex.unlock()
        eat(savage_id)
        shared.barrier1.wait(last="\n")


def chef(chef_id, shared, m):
    while True:
        shared.chef_barrier.wait(each=f"Chef {chef_id} sleeping")
        shared.chef_barrier2.wait(each=f"Chef {chef_id} wake up")
        if shared.empty_pot.value() == 1:
            shared.empty_pot.wait()
            cook(shared, m, chef_id)
        else:
            continue


def run_model(n, m, c):
    savages = list()
    chefs = list()
    shared = SharedObject(n, c)
    for chef_id in range(c):
        chefs.append(Thread(chef, chef_id, shared, m))
    for savage_id in range(n):
        savages.append(Thread(savage, savage_id, shared))

    for t in chefs:
        t.join()

    for t in savages:
        t.join()


if __name__ == "__main__":
    N = 3
    M = 3
    C = 3
    run_model(N, M, C)


