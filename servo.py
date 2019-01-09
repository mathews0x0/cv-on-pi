import RPi.GPIO as GPIO                                 ## Import GPIO Library.
import time                                 ## Import ‘time’ library for a delay.
GPIO.setmode(GPIO.BOARD)                    ## Use BOARD pin numbering.
GPIO.setup(22, GPIO.OUT)                    ## set output.
pwm=GPIO.PWM(22,100)                        ## PWM Frequency
pwm.start(5)
def moveservo(angle):
 if((angle>34)and(angle<101)):
  print(angle)
  duty1= float(angle)/10 + 2.5               ## Angle To Duty cycle  Conversion
  pwm.ChangeDutyCycle(duty1)
  time.sleep(1)
 
 
moveservo(70)
time.sleep(1)
GPIO.cleanup()

