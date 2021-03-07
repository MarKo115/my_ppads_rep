from fei.ppds import Mutex


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



