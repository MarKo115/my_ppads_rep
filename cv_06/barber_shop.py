from fei.ppds import Thread, Semaphore, Mutex, print
from time import sleep
from random import randint


class Helper:
    def __init__(self, c_id):
        self.barber = Semaphore(0)
        self.id = c_id


class SharedObject:
    def __init__(self, n):
        self.mutex = Mutex()
        self.free_chairs = n
        self.queue = []
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customerDone = Semaphore(0)
        self.barberDone = Semaphore(0)


def customer(customer_id, shared):
    while True:
        shared.mutex.lock()
        if shared.free_chairs > 0:
            shared.free_chairs -= 1
            shared.mutex.unlock()

            print(f"Customer {customer_id} arrived at the waiting room.")
            hlp = Helper(customer_id)
            shared.customer.signal()
            shared.queue.append(hlp)
            hlp.barber.wait()

            get_hair_cut(customer_id)

            shared.customerDone.signal()
            shared.barberDone.wait()

            sleep(randint(80, 100) / 10)
        else:
            shared.mutex.unlock()
            balk(customer_id)


def barber(shared):
    while True:
        shared.customer.wait()

        shared.mutex.lock()
        shared.free_chairs += 1
        hlp = shared.queue.pop(0)
        shared.mutex.unlock()

        hlp.barber.signal()
        cut_hair(hlp.id)

        shared.customerDone.wait()
        shared.barberDone.signal()


def get_hair_cut(customer_id):
    print(f"Customer {customer_id}: Fresh haircut.\n")
    sleep(0.2 + randint(0, 2) / 10)


def balk(customer_id):
    print(f"Customer {customer_id} leaving Barber shop without cutting.")
    sleep(randint(20, 40) / 10)


def cut_hair(customer_id):
    print(f"The barber cuts and adjusts the customer {customer_id} hair.")
    sleep(0.5 + randint(0, 5) / 10)


def run_model(n, m):
    threads = list()
    shared = SharedObject(m)
    for customer_id in range(n):
        threads.append(Thread(customer, customer_id, shared))
    threads.append(Thread(barber, shared))

    for t in threads:
        t.join()


if __name__ == "__main__":
    N = 10
    M = 6
    run_model(N, M)


