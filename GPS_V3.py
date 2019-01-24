
import busio
import adafruit_gps
import board

RX = board.RX
TX = board.TX

import serial
uart = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3000)#ttyS0
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')
last_print = time.monotonic()

while true:
    gps.getupdate()
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
    if not gps.has_fix:
        print "fixing..."
        continue
    print "Latitude:",gps.latitude
    print "Logitude:",gps.longitude
    print "Fix quality:",gps.fix_quality
    if gps.satellites is not None:
        print "#satellites:",gps.satellites
    if gps.altitude_m is not None:
        print "Altitude:",gps.altitude_m
    if gps.track_angle_deg is not None:
        print "Speed:",gps.speed_knots
    if gps.track_angle_deg is not None:
        print "Track angle:",gps.track_angle_deg
    if gps.horizontal_dilution is not None:
        print "Horizontal dilution:",gps.horizontal_dilution
    if gps.height_geoid is not None:
        print "Height geo ID:",gps.height_geoid

