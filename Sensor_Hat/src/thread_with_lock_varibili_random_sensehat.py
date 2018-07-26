import threading
import time
from random import randint
from sense_hat import SenseHat
sense = SenseHat()

# Define the colours red and green
red = (255, 0, 0)
green = (0, 255, 0)
black = (0,0,0)
orange = (255, 255, 0)
white = (255,255,255)
blue = (0, 0, 255)

class MyThread (threading.Thread):
   def __init__(self, nome, durata):
      threading.Thread.__init__(self)
      self.nome = nome
      self.durata = durata
   def run(self):
      print ("Thread '" + self.name + "' avviato") 
      time.sleep(self.durata)
      print ("Thread '" + self.name + "' terminato")
     
# Definizione variabili
tempo1 = 100
tempo2 = 100
# tempo3 = 25

# Creazione dei thread
sensori = MyThread("Thread#1", tempo1)
stampa = MyThread("Thread#2", tempo2)
# thread3 = MyThread("Thread#3", tempo3)
 
# Avvio dei thread
sensori.start() 

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

# background
bg = red
      
# colore testo
tx = white
      
# Visualizzazione messaggio scorrevole SenseHat
sense.show_message(message, text_colour=tx, scroll_speed=0.250, back_colour=bg)

# Avvio Thread di stampa a video
stampa.start()
for n in range(1, 6):
      print("ciclo ", str(n))


#thread3.start()

     
# Join
#sensori.join()
#stampa.join()
#thread3.join()


# Fine dello script 

message = "Fine" 

# background
bg = black
      
# colore testo
tx = red

print("Fine")




