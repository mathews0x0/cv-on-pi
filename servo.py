import RPi.GPIO as GPIO                                 ## Import GPIO Library.
import time                                 ## Import ‘time’ library for a delay.
GPIO.setmode(GPIO.BOARD)                    ## Use BOARD pin numbering.
def moveservoy(angle):
 if((angle>34)and(angle<101)):
  print(angle)
  GPIO.setup(22, GPIO.OUT)                    ## set output.
  pwm=GPIO.PWM(22,100)                        ## PWM Frequency
  pwm.start(5)
  duty1= float(angle)/10 + 2.5               ## Angle To Duty cycle  Conversion
  pwm.ChangeDutyCycle(duty1)
  time.sleep(1)
  GPIO.cleanup()
  
  
def moveservox(angle):
 if((angle>0)and(angle<1010)):
  print(angle)
  GPIO.setup(18, GPIO.OUT)                    ## set output.
  pwm=GPIO.PWM(18,100)                        ## PWM Frequency
  pwm.start(5)
  duty1= float(angle)/10 + 2.5               ## Angle To Duty cycle  Conversion
  pwm.ChangeDutyCycle(duty1)
  time.sleep(1)
  GPIO.cleanup()
 
 
moveservoy(95)
print("move y done")
#moveservox()

time.sleep(90)


