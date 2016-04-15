from __future__ import division
import boat_handling
import time
import logging
import sensors_handling
import actuators
import networking

logging.basicConfig(level=logging.INFO,format='%(module)s %(asctime)s %(message)s')


#from sensors import sensors

class Boat_State_Holder(object):
    def __init__(self, Environment_Mode,Operation_Mode):
        
        self.Environment_Mode = Environment_Mode
        self.Operation_Mode = Operation_Mode
        self.Relative_Wind_Angle = None
        self.Absolute_Wind_Angle = None
        self.Sail_1_Hull_Angle = None
        self.Sail_1_Angle_Of_Attack = None
        self.Sail_1_Desired_Hull_Angle = None
        self.Sail_1_Angle_Error_Amount = None        #difference from desired angle to actual angle
        self.Main_Loop_Time_Increment = None
        self.Latitude = None
        self.Longitude = None
        self.GPS_Fix_Time = None #system time when the GPS fix was taken, will differ from the time reported by the GPS.
        self.GPS_Time = None #GPS reported time
        
    def __str__(self):
        """returns a pretty version of the boats state, important stuff only"""
        return "TI : %1.4f R-Wnd-Ang %3.2f S1-Desire %3.2F S1-Hull %3.2F S1-Err %3.2F S1-AoA %3.2f Lat %3.9f Long %3.9f" % (self.Main_Loop_Time_Increment,self.Relative_Wind_Angle,self.Sail_1_Desired_Hull_Angle,self.Sail_1_Hull_Angle,self.Sail_1_Angle_Error_Amount,self.Sail_1_Angle_Of_Attack,self.Latitude , self.Longitude)

        
class boat_executive(object):
    def __init__(self, Environment_Mode,Operation_Mode):
        self.Boat_State = Boat_State_Holder(Environment_Mode,Operation_Mode)        
        self.Operation_Mode = Operation_Mode
        self.Boat_Handler = boat_handling.boat_handling()  
        self.Sensors = sensors_handling.Sensor_Manager(self.Boat_State)
        self.Actuators = actuators.Actuator_Handler(Environment_Mode)
        self.Networking = networking.Network_Manager()
        self._Last_Time = time.time() #watch for long differences between starting this and the first cycle in main loop

        logging.warning('Init boat_executive successfull')        

    def _Time_Increment(self):
        """Returns the time in seconds since this was last called"""
        New_Start = time.time() #need to stick this into a var so you don't loose clock cycles calling time.time twice
        Elapsed_Time = New_Start - self._Last_Time
        self._Last_Time = New_Start
        return Elapsed_Time

        
    def Terminate_Executive(self):
        """Cleanup the sensors and actuators"""
        logging.warning('Shutting Down')
        self.Sensors.Terminate()


        
    def Main_Loop(self):
        """Run the main loop"""
        logging.warning('Main_Loop starting')            
        while (True):
        
            self.Boat_State.Main_Loop_Time_Increment = self._Time_Increment()     
            self.Sensors.Poll_Sensors(self.Boat_State.Main_Loop_Time_Increment , self.Boat_State)
            self.Networking.Poll_Network()
            if (self.Boat_State.Operation_Mode != "Autopilot"):
                pass
            else:   #default to autopilot
                self.Boat_State.Sail_1_Desired_Hull_Angle = self.Boat_Handler.Desired_Sail_1_Angle(self.Boat_State.Relative_Wind_Angle)
                
            self.Actuators.Actuate(self.Boat_State.Main_Loop_Time_Increment, self.Boat_State)
            logging.info(self.Boat_State)                        
            time.sleep(.1)
            #break
        logging.warning('Exited mainloop')
        self.Terminate_Executive()

              
if __name__ == "__main__":
    """We are running the real boat"""
    
    try:
      logging.warning('Running in Physical mode')        
      boat = boat_executive("Physical","Autopilot")
      boat.Main_Loop()
    except KeyboardInterrupt:
      logging.warning('Caught Ctrl+C')
      boat.Terminate_Executive()
      
