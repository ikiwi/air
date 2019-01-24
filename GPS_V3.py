import adafruit_gps

import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)#ttyS0
gps = adafruit_gps.GPS(uart)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')
timestamp = time.monotonic()
while True:
    data = uart.read(32)  # read up to 32 bytes
    # print(data)  # this is a bytearray type
 
    if data is not None:
        # convert bytearray to string
        data_string = ''.join([chr(b) for b in data])
        print(data_string)
 
    if time.monotonic() - timestamp > 5:
        # every 5 seconds...
        gps.send_command(b'PMTK605')  # request firmware version
        timestamp = time.monotonic()
