from __future__ import division
import spidev



spi = spidev.SpiDev()
spi.open(0,0)

def read_wind():
    """Returns relative wind direction to hull, 0-360 degrees"""
    resp = spi.xfer2([0x00,0x00])
    
    angle = ((resp[0] << 9) | (resp[1] << 1)) >> 4
    binary_rep = bin(angle).replace('b','')

#    first_byte = bin(resp[0]).replace('b','')
#    first_byte = first_byte.zfill(8)[-8:]
    
#    second_byte = bin(resp[1]).replace('b','')
#    second_byte = second_byte.zfill(8)[-8:]
    
    compass = (360/4096) * angle
    #print binary_rep.zfill(16), compass, first_byte,second_byte, resp[0],resp[1]
   
    #print "compass %08.2f = angle %08.2f binary %s raw %s" % (compass,angle,binary_rep.zfill(16), resp)
    #time.sleep(.1)
    return compass
    
if __name__ == "__main__":
  """loops at 10hz spitting out rotary angle"""
  import time
  while True:
    print read_wind()
    time.sleep(.1)
    
    
