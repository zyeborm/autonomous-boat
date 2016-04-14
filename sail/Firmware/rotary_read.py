from __future__ import division
import spidev
import logging

class Rotary_Sensors(object):
    def __init__(self):
        logging.info('Init rotary sensors 0')        

        self.spi0 = spidev.SpiDev()
        self.spi0.open(0,0)
        logging.info('Init rotary sensors 1')        
        self.spi1 = spidev.SpiDev()
        self.spi1.open(0,1)

        self.Load_Calibration()
        
    def Load_Calibration(self):
        """Placeholder, use some sort of data storage thing here""" #FIXME
        logging.info('Load Rotary Sensor Calibration')                
        self.Wind_Offset = 0
        self.Sail_1_Offset = 64.07
        
    def Update_Wind_Sensor_Calibration(self,Offset):
        """Store the wind sensor offset"""        
        self.Wind_Offset = Offset

    def Update_Sail_1_Sensor_Calibration(self,Offset):
        """Store the wind sensor offset"""        
        self.Sail_1_Offset = Offset
        
        
    def _convert_to_angle(self,raw_data):
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

    def Read_Wind_Angle_Sensor(self):
        """Returns relative wind direction to hull, 0-360 degrees"""
        resp = self.spi0.xfer2([0x00,0x00])
        return (self._convert_to_angle(resp) + self.Wind_Offset) % 360
        
    def Read_Sail_1_Angle_Sensor(self):
        """Returns absolute sail angle to hull, 0-360 degrees"""
        resp = self.spi1.xfer2([0x00,0x00])
        return (self._convert_to_angle(resp) + self.Sail_1_Offset) % 360
        
if __name__ == "__main__":
    """loops at 10hz spitting out rotary angles"""
    import time
    rotary = Rotary_Sensors()

    while True:
      print "wind : %3.2f   sail %3.2f" % (rotary.Read_Wind_Angle_Sensor(), rotary.Read_Sail_1_Angle_Sensor())
      time.sleep(.1)
        
