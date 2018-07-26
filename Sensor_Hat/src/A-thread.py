import threading
import time

exitFlag = 0

class TestThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        #print ("threadID =" + str(self.threadID) ) 
        #print ("name =" + str(self.name) )
        #print ("counter =" +  str(self.counter) )

        print("Starting " + self.name)
        if self.threadID == 1:
            print_time(self.name, self.counter, 5)
        
        if self.threadID == 2:
           print_counter(self.name, self.counter, 10)

        if self.threadID == 3:
            stampa_stupida(self.name, self.counter, 20)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

def print_counter(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print(threadName, "ciclo", str(counter))
        counter -= 1

def stampa_stupida(threadName, delay, counter):
    while counter:
        print ("Contatore =" + str(counter) )
        counter -= 1 
        
# Create new threads
thread1 = TestThread(1, "Thread 1", 1)
thread2 = TestThread(2, "Thread 2", 2)
thread3 = TestThread(3, "Thread 3", 3)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread1.join()
thread2.join()
thread3.join()
print("Fine del main thread")
