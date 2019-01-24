import time
import datetime
import Adafruit_GPIO.SPI as SPI
import spidev
from firebase import firebase

current_timstamp = str(int(time.time()))

spi = spidev.SpiDev()
spi.open(0,0)
firebase = firebase.FirebaseApplication('https://airquality-8059.firebaseio.com/',None)

def getvalue (channel):
	if channel>7 or channel<0:
		return -1
	op = spi.xfer([1,(8+channel) << 4, 0])
	out = ((op[1]&3) << 8)  + op[2]
	print ("output: {0:4d} ".format(out))
	result = firebase.put('/S12SD/'+current_timstamp,name='UV',data = "output:{0:4d}".format(out))
	time.sleep (1)

while True:
	getvalue(0)
