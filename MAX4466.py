import spidev

spy = spidev.SpiDev()
spy.open(0,1)

getvalue (channel):
   if channel>7 or channel<0:
      return -1
   if channel == 1:
      op = spi.xfer([1,(8+channel) << 4, 0])
      out = ((op[1]&3) << 8)  + op[2]
      print("Sound level",out)

while True:
   getvalue(1)
