from fei.ppds import Mutex
from fei.ppds import Semaphore
from fei.ppds import Thread
from fei.ppds import print
from time import sleep
from random import randint


class ADTLightswitch:
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            sem.wait()
        self.mutex.unlock()

    def unlock(self, sem):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            sem.signal()
        self.mutex.unlock()


def fnc_read(thread_id):
    sleep(randint(1, 10) / 10)
    print(f"{thread_id} reading")


def fnc_write(thread_id):
    sleep(randint(1, 10) / 10)
    print(f"{thread_id} writing")


def readers_light_switch(light_switch, room_e, reader_id):
    light_switch.lock(room_e)
    fnc_read(reader_id)
    light_switch.unlock(room_e)


def writers_light_switch(room_e, writer_id):
    room_e.wait()
    fnc_write(writer_id)
    room_e.signal()


num_r = 10
arr_readers = [0] * num_r
num_w = 10
arr_writers = [0] * num_w
adt_lightswitch = ADTLightswitch()
empty_room = Semaphore(1)

for j in range(num_w):
    arr_writers[j] = Thread(writers_light_switch, empty_room, j)

for i in range(num_r):
    arr_readers[i] = Thread(readers_light_switch, adt_lightswitch, empty_room, i+50)

for t in arr_writers:
    t.join()

for t in arr_readers:
    t.join()

