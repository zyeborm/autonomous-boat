from __future__ import division
from Adafruit_PWM_Servo_Driver import PWM
import time
from rotary_read import read_wind

def sensors(object):
  def __init__(self):
  self.pwm = PWM(0x40)
  # Note if you'd like more debug output you can instead run:
  #pwm = PWM(0x40, debug=True)
  self.Sail1_ServoMin = 360  # Min pulse length out of 4096
  self.Sail1_SservoMax = 480

  def 
  servo_units_per_degree = (servoMax - servoMin) / 360 * 2
  serv_center = ((servoMax - servoMin) / 2) + servoMin
