from __future__ import division
from Adafruit_PWM_Servo_Driver import PWM
import time
from rotary_read import read_wind
import boat_handling

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)


servoMin = 423 #150  # Min pulse length out of 4096
servoMax = 539

servo_units_per_degree = (servoMax - servoMin) / 360 * 2
serv_center = ((servoMax - servoMin) / 2) + servoMin + 2

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

servo_history = 0
backlash_servo_out = 0
servo_hysteresis = 0
while (True):
  # Change speed of continuous servo on channel O
  wind_angle = (read_wind() - 4) % 360 #calibration

  if (wind_angle < -180):
    wind = wind_angle + 360   

  if (wind_angle > 180):
    wind = wind_angle - 360
  else:
    wind=wind_angle
      
  sail_angle = wind 
  servo_out = int(serv_center + sail_angle * servo_units_per_degree)
#  if (servo_out < servo_history):
#    servo_hysteresis = 2
#    print 'bl'
  
#  if servo_hysteresis > 0:
#    backlash_servo_out = servo_out - 5
#    servo_hysteresis -= 1
#  else:

  backlash_servo_out = servo_out

  servo_history = servo_out
  print "wind_angle %.2f sail_angle %.2f difference %.2f servo_out %s backlash_servo_out %s hysteresis %s" % (wind_angle,sail_angle % 360, (wind_angle - sail_angle) % 360 ,servo_out,backlash_servo_out,servo_hysteresis)
  pwm.setPWM(0, 0, int(backlash_servo_out))
  time.sleep(.1)
  
#boat_handler = boat_handling()





