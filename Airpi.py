from firebase import firebase
firebase = firebase.FirebaseApplication('https://airquality-8059.firebaseio.com/',None)

import time
import datetime




current_timstamp = str(int(time.time()))


#CCS811

    from Adafruit_CCS811 import Adafruit_CCS811

    ccs = Adafruit_CCS811 ()
    
    while not ccs.available():
                                pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0


	

	time.sleep(0.5)


#GUVA-S12SD

    import spidev

    spi = spidev.Spidev()
    spi.open(0,0)
    def readadc(adcnum):
        if adcnum > 7 or adcnum < 0:
            return -1
        r = spi.xfer2([1, 8 + adcnum << 4, 0])
        adcout = ((r[1] & 3) << 8) + r[2]
        return adcout
        

    
	op = spi.xfer([1,(8+channel) << 4, 0])
	out = ((op[1]&3) << 8)  + op[2]
	print ("output: {0:4d} ".format(out))
	result = firebase.put('/S12SD/'+current_timstamp,name='UV',data = "output:{0:4d}".format(out))
	time.sleep (1)








#Loop
	
    while True:

        #CCS811
	if ccs.available():

		temp = ccs.calculateTemperature()
		period = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))

		if not ccs.readData():
			print "CO2", ccs.geteCO2(),"	" , "TVOC", ccs.getTVOC()," 	", "Temp", temp, "	"
			print period
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
	S12SD_Volts = (S12SD * 3.3) / 1024
	print ("%4d/1023 => %5.3f V" % (S12SD_Raw, S12SD_Volts))
	result = firebase.put('/data/'+current_timstamp,name='S12SD_Raw',data = S12SD_Raw)
	result = firebase.put('/data/'+current_timstamp,name='S12SD_Volts',data = S12SD_Volts)


        #Max4466
        
	
        #time interval 
	time.sleep(0.5)
