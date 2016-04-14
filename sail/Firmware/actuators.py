from __future__ import division
import time
import logging


class Actuator_Handler(object):
    def __init__(self,Environment_Mode):
        if (Environment_Mode == "Physical"):  #Running on the real boat interface with the hardware
            logging.info('Init servo output') 
            from Adafruit_PWM_Servo_Driver import PWM
            self.pwm = PWM(0x40)              # Initialise the PWM device using the default address
            # Note if you'd like more debug output you can instead run:
            #pwm = PWM(0x40, debug=True)
            self.pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

        self.Sail1Servo = {}
        self.Sail1Servo["ServoMin"] = 423  # Min pulse length out of 4096
        self.Sail1Servo["ServoMax"] = 539  # for +- 90 degrees of travel
        self._Servo_Update_Constants(self.Sail1Servo)
  
    def _Servo_Update_Constants(self,Servo):
        Servo["Servo_Units_Per_Degree"] = (Servo["ServoMax"] - Servo["ServoMin"]) / 360 * 2
        Servo["Servo_Center"] = ((Servo["ServoMax"] - Servo["ServoMin"]) / 2) + Servo["ServoMin"]
    
    def Actuate(self,Time_Increment,Boat_State):
        if (Boat_State.Environment_Mode == "Physical"):  
            self.pwm.setPWM(0, 0, int(self.Sail1Servo["Servo_Center"] + Boat_State.Sail_1_Desired_Hull_Angle * self.Sail1Servo["Servo_Units_Per_Degree"])) #Sail1
          
        
    def setServoPulse(channel, pulse):
      pulseLength = 1000000                   # 1,000,000 us per second
      pulseLength /= 60                       # 60 Hz
      print "%d us per period" % pulseLength
      pulseLength /= 4096                     # 12 bits of resolution
      print "%d us per bit" % pulseLength
      pulse *= 1000
      pulse /= pulseLength
      pwm.setPWM(channel, 0, pulse)


"""while (True):
  # Change speed of continuous servo on channel O
  wind_angle = read_wind()
  sail_angle = boat_handler.desired_sail_angle(wind_angle)
  print "wind_angle %.2f sail_angle %.2f servo_out %s" % (wind_angle,sail_angle,int(serv_center + sail_angle * servo_units_per_degree))
  pwm.setPWM(0, 0, int(serv_center + sail_angle * servo_units_per_degree))
  time.sleep(.1)
 # pwm.setPWM(0, 0, servoMax)
 # time.sleep(1)
"""


