from __future__ import division
import time
import rotary_read 
import gps_read # Needs special treatment because its threaded which is stupid anyway
import logging
#import threading

global gpsd
class Sensor_Manager(object):
    def __init__(self,Boat_State):
        logging.info('Init Sensors')
        self.rotary = rotary_read.Rotary_Sensors()
        if (Boat_State.Environment_Mode == "Physical"):
            pass
            
    def _Anglular_Difference(self,target_heading,actual_heading):
       angle_diff = target_heading - actual_heading
       #print angle_diff
       angle_diff = (angle_diff +180 ) % 360-180
       #print angle_diff
       return angle_diff
       
    def Terminate(self):    
        logging.warning('Terminating GPS Thread')   
        gps_read.gpsp.running = False
        gps_read.gpsp.join(2) # wait up to 2 seconds for the thread to finish what it's doing
        if gps_read.gpsp.isAlive():
            logging.critical('GPS Thread failed to stop after 2 seconds')   
            #FIXME use OS functions to kill the thread
        logging.warning('Terminating GPS Thread - Success')   

    def Poll_Sensors(self,Time_Increment,Boat_State):
        """Read the sensor inputs and perform any massaging needed"""

        #Boat_State.Relative_Wind_Angle = self.rotary.Read_Wind_Angle_Sensor()
        wind_angle = self.rotary.Read_Wind_Angle_Sensor()
        wind_delta = self._Anglular_Difference(wind_angle,Boat_State.Relative_Wind_Angle)
        print Boat_State.Relative_Wind_Angle, wind_angle, wind_delta, wind_delta * .3
        
        Boat_State.Relative_Wind_Angle = (Boat_State.Relative_Wind_Angle  + wind_delta * .3) % 360
        #do magic maths to get absolute wind here
        Boat_State.Sail_1_Hull_Angle = self.rotary.Read_Sail_1_Angle_Sensor()
        Boat_State.Sail_1_Angle_Of_Attack = Boat_State.Relative_Wind_Angle - Boat_State.Sail_1_Hull_Angle
        
        if Boat_State.Sail_1_Desired_Hull_Angle is not None:
            Boat_State.Sail_1_Angle_Error_Amount = (Boat_State.Sail_1_Desired_Hull_Angle % 360) - Boat_State.Sail_1_Hull_Angle
        else:
            Boat_State.Sail_1_Angle_Error_Amount = 0
            
        Boat_State.Latitude = gps_read.gpsd.fix.latitude
        Boat_State.Longitude = gps_read.gpsd.fix.longitude
        Boat_State.GPS_Fix_Time = time.time()
        Boat_State.GPS_Time = gps_read.gpsd.fix.time
 
