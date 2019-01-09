
import time
 
import pigpio
 
servos = 22 #GPIO number
 
pi = pigpio.pi()
#pulsewidth can only set between 500-2500
try:
    while True:
 
        pi.set_servo_pulsewidth(servos, 880) #0 degree
        print("Servo {} {} micro pulses".format(servos, 880))
        time.sleep(1)
        pi.set_servo_pulsewidth(servos, 1200) #90 degree
        print("Servo {} {} micro pulses".format(servos, 1200))
        time.sleep(1)
        pi.set_servo_pulsewidth(servos, 1800) #180 degree
        print("Servo {} {} micro pulses".format(servos, 1800))
        time.sleep(1)
        pi.set_servo_pulsewidth(servos, 1200)
        print("Servo {} {} micro pulses".format(servos, 1200))
        time.sleep(1)
 
   # switch all servos off
except KeyboardInterrupt:
    pi.set_servo_pulsewidth(servos, 0);
 
pi.stop()