import RPi.GPIO as GPIO
import time

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)  # set board mode to BOARD

GPIO.setup(16, GPIO.OUT)  # set up pin 17
#GPIO.setup(18, GPIO.OUT)  # set up pin 18
try:
  while (1==1):
    print 1
    GPIO.output(16, 1)  # turn on pin 17
    #GPIO.output(18, 1)  # turn on pin 18

    time.sleep(1)
    print 0
    GPIO.output(16, 0)  # turn off pin 17
    time.sleep(1)  
    
except:
  pass

GPIO.cleanup()
