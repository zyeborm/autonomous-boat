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

servoMin = 360  # Min pulse length out of 4096
servoMax = 478

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
<<<<<<< HEAD:sail/Firmware/firmware_hack/wind_at_11.py
servo_history = 0
backlash_servo_out = 0
servo_hysteresis = 0
while (True):
  # Change speed of continuous servo on channel O
  wind_angle = (read_wind() - 4) % 360 #calibration
  
  sail_angle = desired_sail_angle(wind_angle)
  servo_out = int(serv_center + sail_angle * servo_units_per_degree)
  if (servo_out < servo_history):
    servo_hysteresis = 5
    print 'bl'
  
  if servo_hysteresis > 0:
    backlash_servo_out = servo_out - 10
    servo_hysteresis -= 1
  else:
    backlash_servo_out = servo_out

  servo_history = servo_out
  print "wind_angle %.2f sail_angle %.2f difference %.2f servo_out %s backlash_servo_out %s hysteresis %s" % (wind_angle,sail_angle % 360, (wind_angle - sail_angle) % 360 ,servo_out,backlash_servo_out,servo_hysteresis)
  pwm.setPWM(0, 0, int(backlash_servo_out))
=======
#boat_handler = boat_handling()

while (True):
  # Change speed of continuous servo on channel O
  wind_angle = read_wind()
  sail_angle = boat_handler.desired_sail_angle(wind_angle)
  print "wind_angle %.2f sail_angle %.2f servo_out %s" % (wind_angle,sail_angle,int(serv_center + sail_angle * servo_units_per_degree))
  pwm.setPWM(0, 0, int(serv_center + sail_angle * servo_units_per_degree))
>>>>>>> d56b23794864b6c8bc723c6e88408e8e72932b2f:sail/Firmware/wind_at_11.py
  time.sleep(.1)
 # pwm.setPWM(0, 0, servoMax)
 # time.sleep(1)



