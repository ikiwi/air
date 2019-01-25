#Firebase Connection
from firebase import firebase
firebase = firebase.FirebaseApplication('https://airquality-8059.firebaseio.com/',None)

import time
import datetime

#CCS811
from Adafruit_CCS811 import Adafruit_CCS811
ccs = Adafruit_CCS811()
while not ccs.available():
                          pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0

#MCP3008 Channels
import spidev
spi = spidev.SpiDev()
spi.open(0,0)

#Max4466 Setup
int peak_to_peak
int signalmax
signalmin = 1024


def readadc(adcnum):
        if adcnum > 7 or adcnum < 0:
            return -1
        r = spi.xfer2([1, 8 + adcnum << 4, 0])
        adcout = ((r[1] & 3) << 8) + r[2]
        return adcout

#Loop
while True:
	
        #Define Time-stamp
	current_timstamp = str(int(time.time()))	
	
	#CCS811
	if ccs.available():
		temp = ccs.calculateTemperature()
		period = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
		if not ccs.readData():
			print ("CO2", ccs.geteCO2(),"	" , "TVOC", ccs.getTVOC()," 	", "Temp", temp, "	")
			print (period)
			result = firebase.put('/data/' + current_timstamp ,name='Time',data = period)
			result = firebase.put('/data/' + current_timstamp ,name='CO2', data = ccs.geteCO2())
			result = firebase.put('/data/' + current_timstamp ,name='TVOC',data = ccs.getTVOC())
			result = firebase.put('/data/' + current_timstamp ,name='Temperature',data = temp)
		else:
			print ("ERROR!")
			while(1):
				 pass
			
	#GUVA-S12SD
	S12SD_Raw = readadc(0)
	S12SD_Volts = (S12SD_Raw * 3.3) / 1024
	print ("%4d/1023 => %5.3f V" % (S12SD_Raw, S12SD_Volts))
	result = firebase.put('/data/'+current_timstamp,name='S12SD_Raw',data = S12SD_Raw)
	result = firebase.put('/data/'+current_timstamp,name='S12SD_Volts',data = S12SD_Volts)
	
        #Max4466
	Sound_Values = readadc(1)
	if Sound_Values < 1024:
		if Sound_Values>signalmax:
			signalmax = Sound_Values
		elif Sound_ValuesM<signalmin:
			signalmin = Sound_Values
	peak_to_peak = signalmax - signalmin
	Sound_Volts = (peak_to_Peak * 5.0) / 1024
	print (peak_to_peak)
	result = firebase.put('/data/'+current_timestamp,name='peak_to_peak',data = peak_to_peak)
	print (Sound_Volts)
	result = firebase.put('/data/'+current_timestamp,name='Sound_Volts',data = Sound_Volts)
	
        #time interval 
	time.sleep(5)
