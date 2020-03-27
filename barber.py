#!/usr/bin/env python
import threading, random, time, sys

# n times barbers
# each barber has one chair that they use when cutting hair
# waiting room with n times chairs
# when done, the barber checks the waiting room, if yes customer goes the barber chair and gets hair cut, else barber return to og chair and sleeps
# customers goes in shop at random, hair cuts takes random amouth of time to complete, when all barbers all occupied customers wait in waiting room
# if customers comes in shop and one or more barber is sleeping, customer wakes one up and sit in their chair

# Note that this problem is based on events. For example, an event happens when a customer enters the shop, and again when s(he) is finished having their hair cut.

class waitingRoom():
    customers = []
    barber = []
    queue = []
    threads = []
    count = 0
    missed = 0
    lock = threading.Lock()
    event = threading.event()
    def __init__(self, chairs=1, barbers=1, names=[]):
        if isinstance(chairs, int) and isinstance(barbers, int):
            self.chairs = chairs
            self.names = names
            for i in range(barbers):
                self.barber.append(Barber(self, str(i) + " " + self.names[random.randint(0, len(self.names) - 1)]))

    def add(self, arg):
        self.count += 1
        if self.chairs != 0:
            # before all that check if there is a barber free
            for i in self.barber:
                if i.sleep():
                    i.wake()
                    t = threading.Thread(target=i.hairCut, args=(self.lock, arg,))
                    self.threads.append(t)
                    t.start()
                    return
            self.customers.append(arg)
            self.chairs -= 1
            self.queue = self.customers[::-1]
        else:
            self.missed += 1

    def next(self):
        if len(self.queue) == 0:
            return None
        else:
            self.chairs += 1
            return self.queue.pop()
    
    def join(self):
        for t in self.threads:
            t.join()

    def status(self):
        print("====================")
        print("barbers   = ", len(self.barber))
        print("customers = ", self.count)
        print("missed    = ", self.missed)
        print("queue     = ", len(self.queue))
        c = 0
        for j in (self.barber):
            if j.sleep():
                c += 1
        print("Sleeping  = ", c)
        print("chairs    = ", self.chairs)
        print("====================\n")


# customer class, require the name and time need to do the hair cut of the customer
class Customer():
    def __init__(self, time, name=None):
        self.name = name
        self.time = time
    
    def time(self):
        return self.time
    
    def name(self):
        return self.name

class Barber():
    s = True
    def __init__(self, shop, name=""):
        self.name = name
        self.shop = shop
    
    def sleep(self):
        return self.s
    
    def wake(self):
        self.s = False
    
    def hairCut(self, lock, arg):
        lock.acquire()
        try:
            if self.s is False:
                time.sleep(arg.time)
                while True:
                    look = self.shop.next()
                    if look != None:
                        time.sleep(look.time)
                        self.shop.status()
                    else:
                        self.s = True
                        self.shop.status()
                        break
        finally:
            lock.release()

if __name__ == "__main__":
    names = ["alan", "tom", "jeff", "gary", "chris", "stev", "donal", "alex", "josh", "jack", "may", "tuff", "bob", "henry", "gluss", "rick", "mick", "rob"]
    customers = []

    for i in range(100):
        i = Customer(random.randint(1,5), names[random.randint(0,len(names) - 1)] + str(i))
        customers.append(i)

    shop = waitingRoom(5, 4, names)

    for i in range(len(customers)):
        start_time = time.time()
        t = random.randint(0, 2)
        time.sleep(t)
        shop.add(customers[i])
        shop.status()
    shop.join()
    shop.status()

    print("--- %s seconds ---" % (time.time() - start_time))

