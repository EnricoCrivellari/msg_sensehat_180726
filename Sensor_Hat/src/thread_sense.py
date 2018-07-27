#!/usr/bin/env python
# -*- coding: utf-8 -*

import threading
import time
from random import randint
from sense_hat import SenseHat
sense = SenseHat()


import json

import paho

import paho.mqtt.publish as publish
#  Prova trasmissione messaggio verso broker di test 
#publish.single("paho/test/single", "boo", hostname="test.mosquitto.org")


##################################
###			Timestamp
###	Classe per la gestione della data-ora attuale
### e restuzione del valore in EPOCH ( UNIX management )
import datetime
import time

class TSDataOra():
	# ritorna il valore attuale di epoch in ms = timestamp
	def valoreEpoch(self):
#		return (round(time.time(), 3))
		return (time.time())
		
#	def ConvertiEpoch(self, r_epoch):
#		print ( "Dal valore in EPOCH converti in data e ora corrispondenti" )
#		print (time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(r_epoch)))


##########################################################################
# Struttura dati che è la base dei dati presenti nella lista
class GestDatiSens:
    def __init__(self,addr):
        # Initialize the base #
        self.payload = 10.10   					# misura in C° della lettura sensore
        self.address = addr 					# indirizzo del sensore
        self.qos = "good" 
        self.timestampDevice = 1458949556100	# data/ora della lettura fatta
		
		

##########################################################################
#   Struttura dati del messagggio di COV in modalità Multy Feed / Multi Value
class ObjectCov_Muf_Muv:
    def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)	
 #       return json.dumps(self, default=lambda o: o.__dict__, indent=4)

Cov_Muf_Muv = ObjectCov_Muf_Muv()
Cov_Muf_Muv.timestampDevice = "15000000000"
Cov_Muf_Muv.qos = "good"
Cov_Muf_Muv.values = []
#print(Cov_Muf_Muv.toJSON())



#####################################################################
###  Dichiarazione della Lista contenente le informazioni di ogni 
###  singolo sensore  letto
listmisure = []


#####################################################################
###  Classe per la gestione della formattazzione e creazione vari messaggi MQTT
###  dell'impacchettamento delle lutture dei
###  sensori e trasformazione in un messaggio MQTT completo
class MsgMqtt:

	##  Leggi_dati e estrae dalla lista tutti gli oggetti inseriti nella lista misure	
	def crea_msg_COV_Muf_Muv (self, mqttClientId, lista):
		# Invia tutti gli oggetti dalla coda per formare il messaggio

		# istanzia la classe per data e ora in ephoc ms
		TMSTP = TSDataOra()

		#  Completamento dei campi per il messaggio di tipo COV Multi Feed / Multi Value
		Cov_Muf_Muv.timestampDevice = TMSTP.valoreEpoch()
		Cov_Muf_Muv.values = []
		Cov_Muf_Muv.values = lista
		numero_msg = len(lista)

		# invia il messaggio su terminale
		print("de/"+mqttClientId+"/@DATA"+Cov_Muf_Muv.toJSON())
		
		# pubblica il messaggio verso BROKER
#		publish.single("paho/test/single", "Pippo e Pluto boo", hostname="test.mosquitto.org")
		publish.single("paho/test/single", ("de/"+mqttClientId+"/@DATA"+Cov_Muf_Muv.toJSON()), hostname="test.mosquitto.org")
		
		# Pulisci la lista dai messaggi inviati 
		while numero_msg:
			lista.pop(0)
			numero_msg = len(lista)
	
	def presenza_misure (self, lista):
		if len(lista) == 0:
			return (False)
		else:
			return (True)

		
# Carica il valore letto dal sensore nella lista misure		
def ins_lettura_coda ( misura, address_sens):
	# istanzia la classe per struttura dati lettura singola
	writeSingleData = GestDatiSens(address_sens) # indirizzo del sensore
	# istanzia la classe per data e ora in ephoc ms
	TMSTP = TSDataOra()
	# completa l'inserimento dati
	writeSingleData.payload = misura						# Misura letta
	writeSingleData.timestampDevice = TMSTP.valoreEpoch()	# data-ora in epoch ms attuale
	writeSingleData.qos = "good" 
	listmisure.append(writeSingleData)
	

		 	
			
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
            acq_sensori(self.name, self.counter, 20)
        
        if self.threadID == 2:
            print_time(self.name, self.counter, 10)

        if self.threadID == 3:
            print_counter(self.name, self.counter, 10)

        if self.threadID == 4:
            invio_messaggio(self.name, self.counter, 10)

			
####     Dati al momento statici			
INDIRIZZO_SENS_TEMPERATURA = "0001"
INDIRIZZO_SENS_PRESSIONE = "0002"
INDIRIZZO_SENS_UMIDITA = "0003"

#  DEFINIZIONE  THREAD  ID = 1
#  Dichiarazione di tutte le azioni che devono essere svolte dal THREAD
def acq_sensori(threadName, delay, counter):
	while counter:
		if exitFlag:
			threadName.exit()
		time.sleep(delay)
		print(" Lettura e caricamento misure il: " + "%s: %s" % (threadName, time.ctime(time.time())))
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

		# caricamento lettura nella lista
		ins_lettura_coda(t, INDIRIZZO_SENS_TEMPERATURA)
		ins_lettura_coda(p, INDIRIZZO_SENS_PRESSIONE)
		ins_lettura_coda(h, INDIRIZZO_SENS_UMIDITA)
		
		# str() conversione valori int in string per poterli concatenare 
		message = "Temperature: " + str(t) + "Pressure: " + str(p) + "Humidity: " + str(h)
		
		# Visualizzazione messaggio scorrevole SenseHat
		sense.show_message(message, text_colour=tx, scroll_speed=0.50, back_colour=bg)
		counter -= 1
		

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

#  DEFINIZIONE  THREAD  ID = 4
#  Dichiarazione di tutte le azioni che devono essere svolte dal THREAD
def invio_messaggio(threadName, delay, counter):
	GestMsg = MsgMqtt()
	while counter:
		if exitFlag:
			threadName.exit()
		time.sleep(delay)
		if GestMsg.presenza_misure(listmisure) == True:
			GestMsg.crea_msg_COV_Muf_Muv("DAB_0001",listmisure)
			print(threadName, "Messaggio MQTT", str(counter))
		else:
			print (" Non ci sono misure sensori da inviare" )
		counter -= 1



# Create new threads
thread1 = TestThread(1, "Thread 1", 1)
thread2 = TestThread(2, "Thread 2", 2)
thread3 = TestThread(3, "Thread 3", 3)
thread4 = TestThread(4, "Thread 4", 4)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
print(" -- Fine del main thread  -- ")
