from __future__ import division

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
    
  sailag = 11 #wing angle to wind
  tackag = 15 #boat hard tacking angle
  unsailag =110 #stall angle for wing to wind angle
  runsailag = 90 #runing sail angle to wind
  sailingag=180
  if wind>180 or wind<-180:
      print'wind error',wind
  elif abs(wind)<tackag:
      sailingag =0
      print 'into wind, sail angle',sailingag
  elif wind<0 and abs(wind)>=tackag and abs(wind)<unsailag:
      sailingag=Anglular_adding(wind,sailag)
      print'sail angle..',sailingag#--reach,windward
  elif wind>0 and abs(wind)>=tackag and abs(wind)<unsailag:
      sailingag=Anglular_Difference(wind,sailag)
      print'sail angle',sailingag#++reach,windward
  elif abs(wind)>unsailag and wind<0:
      sailingag=Anglular_adding(wind,runsailag)
      print'sail anglerun..',sailingag#---runnig
  else: 
      sailingag=Anglular_Difference(wind,runsailag)
      print'sail anglerun',sailingag#++running
      print'wind',wind
  print 'end'

  #if (sailingag < 0):
  #    sailingag = sailingag + 360
  return sailingag
