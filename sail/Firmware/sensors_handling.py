from __future__ import division
import time
import rotary_read 

class Sensor_Manager(object):
    def __init__(self):
        self.rotary = rotary_read.Rotary_Sensors()
#        self.Relative_Wind_Angle = 0
#        self.Absolute_Wind_Angle = 0

    def Poll_Sensors(self,Time_Increment,Boat_State):
        """Read the sensor inputs and perform any massaging needed"""
        Boat_State.Relative_Wind_Angle = self.rotary.Read_Wind_Angle_Sensor()
        #do magic maths to get absolute wind here
        Boat_State.Sail_1_Hull_Angle = self.rotary.Read_Sail_1_Angle_Sensor()
        Boat_State.Sail_1_Angle_Of_Attack = Boat_State.Relative_Wind_Angle - Boat_State.Sail_1_Hull_Angle
