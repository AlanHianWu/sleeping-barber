#!/usr/bin/env python
import threading, random, time, queue

# varibles declared here, you can specify the amouth of barbers, customers, chairs and how busy it will be
# note the the busy varible determines the rate at wich the customers come in. 0 for when they all come in at once
barber, customers, chairs, busy = 10, 50, 15, 0

# the queue is set with maxsize at barber + chairs, at minium all the barbers at have their own chairs
queue = queue.Queue(maxsize=barber + chairs)

class Barber(threading.Thread):
    global queue
    def __init__(self, condition, event):
        threading.Thread.__init__(self)
        self.condition = condition
        self.end = event

    def run(self):
        while True:
            if self.end.isSet():
                print(threading.currentThread(), "going home")
                return
            with self.condition:
                if queue.empty():
                    print(threading.currentThread(), "sleep")
                    self.condition.wait()
                    if self.end.isSet():
                        print(threading.currentThread(), "going home")
                        return
                c = queue.get()
            print(threading.currentThread(), "cutting", c)
            time.sleep(c.time)

class Customer(threading.Thread):
    global queue
    def __init__(self, condition, c):
        threading.Thread.__init__(self)
        self.time = random.randint(2, 5)
        self.serviced = condition
        self.c = c

    def time(self):
        return self.time
    
    def order(self):
        return self.c

    def run(self):
        with self.serviced:
            if queue.full():
                print("full")
                return
            print(threading.current_thread, "joined")
            queue.put(self)
            self.serviced.notify()

class Shop(threading.Thread):
    global queue

    def __init__(self, Barber=1, Customers=1, fequency=0):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.condition = threading.Condition()
        self.barCount = Barber
        self.cusCount = Customers
        self.Fequency = fequency
        self.BERBARS = []
    
    def open(self):
        print("Shop open for business")
        for b in range(self.barCount):
            b = Barber(self.condition, self.event)
            self.BERBARS.append(b)
            b.start()

        for c in range(self.cusCount):
            time.sleep(self.Fequency)
            Customer(self.condition, c).start()

    def close(self):
        print("Shop closed")
        with self.condition:
            while not queue.empty():
                queue.get()
            self.event.set()
            print("wake up everyone")
            self.condition.notifyAll()
        for b in self.BERBARS:
            print(b, "leaving")
            b.join()

def main():
    shop = Shop(barber, customers, busy)
    shop.open()
    # this time.sleep() gives time for the shop to be open before closing, kind of like opening hours
    time.sleep(2)
    shop.close()

if __name__ == "__main__":
    main()