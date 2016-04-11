from __future__ import division

class boat_handling(object):
  def __init__(self):
    self.sailag = 11 #wing angle to wind
    self.tackag = 45 #boat hard tacking angle
    self.unsailag =110 #stall angle for wing to wind angle
    self.runsailag = 90 #runing sail angle to wind
    

  def Anglular_Difference (target_heading,actual_heading):
      angle_diff = target_heading - actual_heading
      #print angle_diff
      angle_diff = (angle_diff +180 ) % 360-180
      #print angle_diff
      return angle_diff
      
  def Anglular_adding (target_heading,actual_heading):
      angle_diff = target_heading + actual_heading
      #print' add', angle_diff
      angle_diff = (angle_diff + 180) % 360 - 180
      #print 'add2',angle_diff
      return angle_diff
      
  def desired_sail_angle(relative_wind):
    """takes in + - 180 degrees"""
    if (relative_wind < -180):
      wind = relative_wind + 360   

    if (relative_wind > 180):
      wind = relative_wind - 360
    else:
      wind=relative_wind #wind angle across deck
      
    sailingag=180
    if wind>180 or wind<-180:
        print'wind error',wind
    elif abs(wind)<self.tackag:
        sailingag =0
        print 'into wind, sail angle',sailingag
    elif wind<0 and abs(wind)>=self.tackag and abs(wind)<self.unsailag:
        sailingag=Anglular_adding(wind,self.sailag)
        print'sail angle..',sailingag#--reach,windward
    elif wind>0 and abs(wind)>=self.tackag and abs(wind)<self.unsailag:
        sailingag=Anglular_Difference(wind,self.sailag)
        print'sail angle',sailingag#++reach,windward
    elif abs(wind)>self.unsailag and wind<0:
        sailingag=Anglular_adding(wind,self.runsailag)
        print'sail anglerun..',sailingag#---runnig
    else: 
        sailingag=Anglular_Difference(wind,self.runsailag)
        print'sail anglerun',sailingag#++running
        print'wind',wind
    print 'end'

    #if (sailingag < 0):
    #    sailingag = sailingag + 360
    return sailingag


  def desired_heading_angle(relative_wind,course):
    heading = course
    return heading
    
    

