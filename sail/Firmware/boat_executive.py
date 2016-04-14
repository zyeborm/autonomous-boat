from __future__ import division
from boat_handling import boat_handling
import time
import logging

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')


#from sensors import sensors



class boat_executive(object):
    def __init__(self, Operation_Mode):
        self.Operation_Mode = Operation_Mode
        boat_handler = boat_handling()  
        logging.warning('Init boat_executive successfull')        
        

    def Terminate_Executive(self):
        """Cleanup the sensors and actuators"""
        logging.warning('Shutting Down')
        pass
        
    def Main_Loop(self):
        """Run the main loop"""
        logging.warning('Main_Loop starting')            
        while (True):
            time.sleep(.1)

              
if __name__ == "__main__":
    """We are running the real boat"""
    
    try:
      logging.warning('Running in Physical mode')        
      boat = boat_executive("Physical")
      boat.Main_Loop()
    except KeyboardInterrupt:
      logging.warning('Caught Ctrl+C')
      boat.Terminate_Executive()
      
