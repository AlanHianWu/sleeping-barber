#!/usr/bin/env python
import threading, random, time, queue

# n times barbers
# each barber has one chair that they use when cutting hair
# waiting room with n times chairs
# when done, the barber checks the waiting room, if yes customer goes the barber chair and gets hair cut, else barber return to og chair and sleeps
# customers goes in shop at random, hair cuts takes random amouth of time to complete, when all barbers all occupied customers wait in waiting room
# if customers comes in shop and one or more barber is sleeping, customer wakes one up and sit in their chair

# Note that this problem is based on events. For example, an event happens when a customer enters the shop, and again when s(he) is finished having their hair cut.

class waitingRoom():
    barber = []
    queue = queue.Queue()
    threads = []
    count = 0
    missed = 0
    lock = threading.Lock()
    lock2 = threading.Lock()
    def __init__(self, chairs=1, barbers=1, names=[]):
        if isinstance(chairs, int) and isinstance(barbers, int):
            self.chairs = chairs
            self.names = names
            for i in range(barbers):
                self.barber.append(Barber(self, str(i) + " " + self.names[random.randint(0, len(self.names) - 1)]))

    def add(self, arg):
        self.count += 1
        if self.chairs != 0:
            with self.lock:
                for i in self.barber:
                    if i.sleep():
                        i.wake()
                        thread = threading.Thread(target=i.hairCut, args=(arg,))
                        self.threads.append(thread)
                        print(self.threads)
                        thread.start()
                        return
                self.chairs -= 1
                self.queue.put(arg)
        else:
            self.missed += 1

    def next(self):
        with self.lock2:
            self.chairs += 1
            return self.queue.get()
    
    def hasNext(self):
        return self.queue.empty()

    def join(self):
        for t in self.threads:
            t.join()

    def status(self):
        print("====================")
        print("barbers   = ", len(self.barber))
        print("customers = ", self.count)
        print("missed    = ", self.missed)
        print("queue     = ", self.queue.qsize())
        c = 0
        for j in (self.barber):
            if not j.sleep():
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
    event = threading.Event()
    def __init__(self, shop, name=""):
        self.name = name
        self.shop = shop
  
    def sleep(self):
        return not self.event.isSet()
    
    def wake(self):
        self.event.set()

    def hairCut(self, arg):
        if self.event.isSet():
            time.sleep(arg.time)
            while not self.shop.hasNext():
                self.shop.status()
                c = self.shop.next()
                time.sleep(self.shop.next().time)
            self.event.clear()

if __name__ == "__main__":
    names = ["alan", "tom", "jeff", "gary", "chris", "stev", "donal", "alex", "josh", "jack", "may", "tuff", "bob", "henry", "gluss", "rick", "mick", "rob"]
    customers = []
    for i in range(20):
        i = Customer(random.randint(1,4), names[random.randint(0,len(names) - 1)] + str(i))
        customers.append(i)

    shop = waitingRoom(10, 4, names)

    for i in range(len(customers)):
        start_time = time.time()
        t = random.randint(0, 2)
        time.sleep(t)
        shop.add(customers[i])
        shop.status()
    print("joining")
    shop.join()
    print("after join")
    shop.status()

    print("--- %s seconds ---" % (time.time() - start_time))

