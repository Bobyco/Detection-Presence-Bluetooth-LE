# bluetooth low energy scan
from bluetooth.ble import DiscoveryService
import time
import RPi.GPIO as GPIO
import os

# Configuration
mac = "EA:91:0F:D0:E2:57" # Adresse Mac a detecter.
delaiNonPresence = 15 # Delai auquel le scripte doit effectuer une action quand l'adresse mac n'est pas detecter.
delaiPresence = 15 # Delai auquel le scripte doit effectuer une action quand l'adresse mac est detecter.
delaiScan = 10 # Durer du scan.
gpioControle = 2 # GPIO a controler.
#Fin de configuration


GPIO.setwarnings(False) # Desactivation des warnings
GPIO.setmode(GPIO.BCM) # Numerotation BCM
GPIO.setup(gpioControle, GPIO.OUT, initial=GPIO.LOW) # Initialisation du GPIO

colors = {'gris': 30, 'rouge': 31, 'vert': 32, 'jaune': 33, 'blue': 34, 'magenta': 35, 'cyan': 36, 'blanc': 37}

def couleur(choixCouleur):
	print ("\033[1;%d;40m" %(colors.get(choixCouleur)))

print ("Adresse a detecter : %s -- GPIO a controler : %s" %(mac, gpioControle))
print ("Durer du scan : %s -- Confirmation de presence %s -- Confirmation de non presence %s" %(delaiScan, delaiPresence, delaiNonPresence))



timeNonPresent = 0
timePresent = 0
compteurBoucle = 0
boolNonPresence = 0

while True:


	couleur("blanc")
	print ("-------------------------------------------------")
	print ("Boucle numero: %s" % compteurBoucle)
	print (time.strftime("%H:%M:%S - Debut du scan ...")) #Affichage de l'heur.
	print ("timePresent : %d --- timeNonPresent : %d" %(timePresent,timeNonPresent))
	startTime = time.time() # Debut du chrono.

	boolNonPresence = 0 # Mise a zero du compteur de presence pendant la boucle.
	boolPresence = 0 # Mise a zero du compteur de presence pendant la boucle.

	service = DiscoveryService()
	devices = service.discover(delaiScan)

	couleur("magenta")

	for address, name in devices.items():

	        print("name: {}, address: {}".format(name, address))

		if (address == mac): # Adresse mac detecter
			couleur("cyan")
			print ("L'adresse numero " + mac + " a etait detecter")
			stopTime = time.time()
			timePresent = (timePresent + int(stopTime - startTime))

			print("timePresent %s" % timePresent)
			print("timeNonPresent %s" % timeNonPresent)

			boolNonPresence = 0

			if timePresent >= delaiPresence:
				couleur("jaune")
				print ("Presence confirmer.")
				GPIO.output(gpioControle,GPIO.HIGH)
				break

			else:
				couleur("jaune")
				print("Presence detecter, attente du delai choisie pour confirmation de presence.")
				timeNonPresent = 0
				break

		else:
			if boolNonPresence == 0:
				boolNonPresence = 1


	couleur("blanc")
	print (time.strftime("%H:%M:%S - Fin du scan ..."))
				


	# Si aucune presence detecter pendant le scan.
	if boolNonPresence == 1:
		couleur("jaune") 
		print("Aucune presence detecter pendant le scan")
		stopTime = time.time()
		timeNonPresent = (timeNonPresent + int(stopTime - startTime))
		print("timeNonPresent %s" % timeNonPresent)

	# Si aucune presence pendant le temps choisie.
	if timeNonPresent >= delaiNonPresence:
		couleur("rouge")
		timePresent = 0
		print ("Aucune presence depuis plus de %s secondes" %delaiNonPresence)
		GPIO.output(gpioControle, GPIO.LOW)

	couleur("blanc")

	compteurBoucle = compteurBoucle + 1
	time.sleep(0.1)
