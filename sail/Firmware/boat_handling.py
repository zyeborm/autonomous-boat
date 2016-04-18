from __future__ import division
import logging

class boat_handling(object):
  def __init__(self):
    self.sailag = 11 #wing angle to wind
    self.tackag = 15 #boat hard tacking angle
    self.unsailag =130 #stall angle for wing to wind angle
    self.runsailag = 90 #runing sail angle to wind
    

  def _Anglular_Difference(self,target_heading,actual_heading):
      angle_diff = target_heading - actual_heading
      #print angle_diff
      angle_diff = (angle_diff +180 ) % 360-180
      #print angle_diff
      return angle_diff
      
  def _Anglular_adding(self,target_heading,actual_heading):
      angle_diff = target_heading + actual_heading
      #print' add', angle_diff
      angle_diff = (angle_diff + 180) % 360 - 180
      #print 'add2',angle_diff
      return angle_diff
      
  def Desired_Sail_1_Angle(self,relative_wind):
    """takes in + - 180 degrees"""
    if (relative_wind < -180):
      wind = relative_wind + 360   

    if (relative_wind > 180):
      wind = relative_wind - 360
    else:
      wind=relative_wind #wind angle across deck
      
    sailingag=180
    if wind>180 or wind<-180:
        logging.critical('Wind Error, got %s which is outside +-180',wind)
    elif abs(wind)<self.tackag:
        sailingag = wind
        logging.debug('into wind, sail angle %s',sailingag)
    elif wind<0 and abs(wind)>=self.tackag and abs(wind)<self.unsailag:
        sailingag=self._Anglular_adding(wind,self.sailag)
        logging.debug('sail angle %s',sailingag)
        
    elif wind>0 and abs(wind)>=self.tackag and abs(wind)<self.unsailag:
        sailingag=self._Anglular_Difference(wind,self.sailag)
        logging.debug('sail angle %s',sailingag)
    elif abs(wind)>self.unsailag and wind<0:
        sailingag=self._Anglular_adding(wind,self.runsailag)
        logging.debug('sail angle %s',sailingag)
    else: 
        sailingag=self._Anglular_Difference(wind,self.runsailag)
        logging.debug('sail angle run %s wind %s',sailingag,wind)


    #if (sailingag < 0):
    #    sailingag = sailingag + 360
    return sailingag


  def desired_heading_angle(relative_wind,course):
    heading = course
    return heading
    
    

