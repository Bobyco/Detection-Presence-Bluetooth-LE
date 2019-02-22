# bluetooth low energy scan
from bluetooth.ble import DiscoveryService
import time
import RPi.GPIO as GPIO

mac = "EA:91:0F:D0:E2:57" # Adresse Mac a detecter

co = 0
print co

GPIO.setwarnings(False) # Desactivation des warnings
GPIO.setmode(GPIO.BCM) # Numerotation BCM
GPIO.setup(2, GPIO.OUT, initial=GPIO.LOW) # Initialisation GPIO 2 , OUT et LOW


print "-- Test GPIO ---"
i = 0
while i < 6:
	GPIO.output (2, not GPIO.input(2))
	i = i + 1
	time.sleep(.6)
print "--- Fin Du Test ---"

Presence__NOK = 0

while True:


	service = DiscoveryService()
	devices = service.discover(10)

	print ("-------------------------------------------------")
	print "Boucle N : %s" % co


	for address, name in devices.items():
	        print("name: {}, address: {}".format(name, address))
		if (address == mac):
			print "OK"
			GPIO.output(2,GPIO.HIGH)
			Presence__NOK = 0
			break
		else:
			if Presence__NOK < 30:
				print "NOK"
				Presence__NOK = Presence__NOK + 1
				print "Compteur de non presence : %s" % Presence__NOK
			else:
				print "Compteur de non presence superieur a 30"
				GPIO.output(2, GPIO.LOW)

	co = co + 1
	time.sleep(10)
