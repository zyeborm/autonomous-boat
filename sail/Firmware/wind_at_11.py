from __future__ import division
from Adafruit_PWM_Servo_Driver import PWM
import time
from rotary_read import read_wind
from boat_handling import desired_sail_angle
# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 360  # Min pulse length out of 4096
servoMax = 480

servo_units_per_degree = (servoMax - servoMin) / 360 * 2
serv_center = ((servoMax - servoMin) / 2) + servoMin

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

while (True):
  # Change speed of continuous servo on channel O
  wind_angle = read_wind()
  sail_angle = desired_sail_angle(wind_angle)
  print "wind_angle %.2f sail_angle %.2f servo_out %s" % (wind_angle,sail_angle,int(serv_center + sail_angle * servo_units_per_degree))
  pwm.setPWM(0, 0, int(serv_center + sail_angle * servo_units_per_degree))
  time.sleep(.1)
 # pwm.setPWM(0, 0, servoMax)
 # time.sleep(1)



