from firebase import firebase
import time
import datetime
from Adafruit_CCS811 import Adafruit_CCS811

firebase = firebase.FirebaseApplication('https://airquality-8059.firebaseio.com/',None)

ccs = Adafruit_CCS811 ()
while not ccs.available():
	pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0

while (1):
	if ccs.available():
		temp = ccs.calculateTemperature()
		period = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
		if not ccs.readData():
			print "CO2", ccs.geteCO2(),"	" , "TVOC", ccs.getTVOC()," 	", "Temp", temp, "	"
			print period
			result = firebase.put('/temp/',name='time',data = period)
			result = firebase.put('/temp/',name='CO2', data = ccs.geteCO2())
			result = firebase.put('/temp/',name='TVOC',data = ccs.getTVOC())
			result = firebase.put('/temp/',name='Temp',data = temp)
		else:
			print ("ERROR!")
			while(1):
				pass

	time.sleep(1)

