import threading
import time
from random import randint
from sense_hat import SenseHat
sense = SenseHat()

#Define the colours red and green
red = (255, 0, 0)
green = (0, 255, 0)
black = (0,0,0)
orange = (255, 255, 0)
white = (255,255,255)
blue = (0, 0, 255)

exitFlag = 0

class TestThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        time.sleep(self.counter)
        print("Starting " + self.name)
        if self.threadID == 1:
            acq_sensori(self.name, self.counter, 2)
        
        if self.threadID == 2:
            print_time(self.name, self.counter, 50)

        if self.threadID == 3:
            print_counter(self.name, self.counter, 50)

#  DEFINIZIONE  THREAD  ID = 1
#  Dichiarazione di tutte le azioni che devono essere svolte dal THREAD
def acq_sensori(threadName, delay, counter):
    
    # background
    bg = red
      
    # colore testo
    tx = white

    # Lettura dai sensori del SenseHat acquisizione Temperatura, Pressione, Humidity
    t = sense.get_temperature()
    p = sense.get_pressure()
    h = sense.get_humidity()

    # Arrotondamento ad una cifra decimale
    t = round(t, 1)
    p = round(p, 1)
    h = round(h, 1)

    # str() conversione valori int in string per poterli concatenare 
    message = "Temperature: " + str(t) + "Pressure: " + str(p) + "Humidity: " + str(h)

    # Visualizzazione messaggio scorrevole SenseHat
    sense.show_message(message, text_colour=tx, scroll_speed=0.50, back_colour=bg)

#  DEFINIZIONE  THREAD  ID = 2
#  Dichiarazione di tutte le azioni che devono essere svolte dal THREAD
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

#  DEFINIZIONE  THREAD  ID = 3
#  Dichiarazione di tutte le azioni che devono essere svolte dal THREAD
def print_counter(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print(threadName, "ciclo", str(counter))
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
