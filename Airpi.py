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

#MCP3008 Setup
def readadc(adcnum):
        if adcnum > 7 or adcnum < 0:
            return -1
        r = spi.xfer2([1, 8 + adcnum << 4, 0])
        adcout = ((r[1] & 3) << 8) + r[2]
        return adcout

#Max4466 Setup
peak_to_peak=0
signalmax=0
signalmin = 1024

#DHT22 Setup
import Adafruit_DHT
sensor = Adafruit_DHT.DHT22
pin = '17'

#GPS Setup
import adafruit_gps
import serial

uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3000)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

gps.send_command(b'PMTK220,1000')
last_print = time.monotonic()

#BME280 Setup
from Adafruit_BME280 import *

BME = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)


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
	
	#Mics 5524
	Gas = readadc(1)
	print( "Gas Level:", Gas)
	result = firebase.put('/data/' + current_timstamp ,name='Gas_Level',data = Gas)

	
        #Max4466
	Sound_Values = readadc(2)
	if Sound_Values < 1024:
		if Sound_Values>signalmax:
			signalmax = Sound_Values
		elif Sound_Values<signalmin:
			signalmin = Sound_Values
	peak_to_peak = signalmax - signalmin
	Sound_Volts = (peak_to_peak * 5.0) / 1024
	print (peak_to_peak)
	result = firebase.put('/data/'+current_timstamp,name='peak_to_peak',data = peak_to_peak)
	print (Sound_Volts)
	result = firebase.put('/data/'+current_timstamp,name='Sound_Volts',data = Sound_Volts)
	
	#GA1A12S202
	Light = readadc(3)
	print("Light Level:", readadc(3))
	result = firebase.put('/data/' + current_timstamp ,name='Light_Level',data = Light)

	
	#DHT22
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
    		print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
	else:
    		print('Failed to get reading. Try again!')
	result = firebase.put('/data/' + current_timstamp ,name='DHT_Temperature',data = temperature)
	result = firebase.put('/data/' + current_timstamp ,name='Humidity',data = humidity)

	#GPS
	gps.update()
	current = time.monotonic()
	if current - last_print >= 1.0:
		last_print = current
	if not gps.has_fix:
		print("fixing")
		continue
	print('Latitude: {0:.6f} degrees'.format(gps.latitude))
	print('Longitude: {0:.6f} degrees'.format(gps.longitude))
	
	result = firebase.put('/data/' + current_timstamp ,name='Latitude',data = gps.latitude)
	result = firebase.put('/data/' + current_timstamp ,name='Longitude',data = gps.longitude)

	print('Fix quality: {}'.format(gps.fix_quality))
	if gps.satellites is not None:
		print('# satellites: {}'.format(gps.satellites))
	if gps.altitude_m is not None:
		print('Altitude: {} meters'.format(gps.altitude_m))
	if gps.track_angle_deg is not None:
		print('Speed: {} knots'.format(gps.speed_knots))
	if gps.track_angle_deg is not None:
		print('Track angle: {} degrees'.format(gps.track_angle_deg))
	if gps.horizontal_dilution is not None:
		print('Horizontal dilution: {}'.format(gps.horizontal_dilution))
	if gps.height_geoid is not None:
		print('Height geo ID: {} meters'.format(gps.height_geoid))
	
	#BME280
	bme_degrees = BME.read_temperature()
	pascals = BME.read_pressure()
	hectopascals = pascals / 100
	bme_humidity = BME.read_humidity()
	
	print("BME Temp:",bme_degrees)
	print("Pressure:",hectopascals)
	print("BME Humidity:",bme_humidity)
	result = firebase.put('/data/' + current_timstamp ,name='BME_Temp',data = bme_degrees)
	result = firebase.put('/data/' + current_timstamp ,name='Pressure',data = hectopascals)
	result = firebase.put('/data/' + current_timstamp ,name='BME_Humidity',data = bme_humidity)
	
        #time interval 
	time.sleep(5)
