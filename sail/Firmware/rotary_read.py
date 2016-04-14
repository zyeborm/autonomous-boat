from __future__ import division
import spidev



spi0 = spidev.SpiDev()
spi0.open(0,0)

spi1 = spidev.SpiDev()
spi1.open(0,1)
def _convert_to_angle(raw_data):
    """Converts 2 byte input to an angle in degrees"""

    angle = ((raw_data[0] << 9) | (raw_data[1] << 1)) >> 4
    #binary_rep = bin(angle).replace('b','')

#    first_byte = bin(resp[0]).replace('b','')
#    first_byte = first_byte.zfill(8)[-8:]
    
#    second_byte = bin(resp[1]).replace('b','')
#    second_byte = second_byte.zfill(8)[-8:]
    
    compass = (360/4096) * angle
    #print binary_rep.zfill(16), compass, first_byte,second_byte, resp[0],resp[1]
   
    #print "compass %08.2f = angle %08.2f binary %s raw %s" % (compass,angle,binary_rep.zfill(16), resp)
    #time.sleep(.1)
    return compass

def read_wind():
    """Returns relative wind direction to hull, 0-360 degrees"""
    resp = spi0.xfer2([0x00,0x00])
    return _convert_to_angle(resp)
    
def read_sail():
    """Returns absolute sail angle to hull, 0-360 degrees"""
    resp = spi1.xfer2([0x00,0x00])
    return _convert_to_angle(resp)
    
if __name__ == "__main__":
  """loops at 10hz spitting out rotary angles"""
  import time
  while True:
    print "wind : %3.2f   sail %3.2f" % (read_wind(), read_sail())
    time.sleep(.1)
    
