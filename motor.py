import RPi.GPIO as GPIO
from time import sleep

# must instsall RPi.GPIO see README.md under to set up

GPIO.cleanup()
# sets variables to input/output pins
# take a look at this:
# https://github.com/vishytheswishy/junk-transporter-backend/blob/main/motor.py
ground = 6
motor_in1 = 23
motor_in2 = 24
motor_enA = 25
lswitch_gpio27 = 27
lswitch_gpio22 = 22
# driver_gpio23 = 16
# driver_gpio24 = 18
voltage5 = 2

# Motor Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_in1, GPIO.OUT)
GPIO.setup(motor_in2, GPIO.OUT)
GPIO.setup(motor_enA, GPIO.OUT)
GPIO.output(motor_in1, GPIO.LOW)
GPIO.output(motor_in2, GPIO.LOW)

pwr =GPIO.PWM(motor_enA, 1000)
pwr.start(25)

# Limit Switch Setup
GPIO.setup(lswitch_gpio27, GPIO.OUT) # in or out
GPIO.setup(lswitch_gpio22, GPIO.OUT) # in or out
GPIO.setup(voltage5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#GPIO.setup(lswitch_gpio22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(lswitch_gpio22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Code found online for changing limit switches

"""
gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(21, gpio.IN, pull_up_down=GPIO.PUD_UP)
 
seconds = 10
print "reverse"
gpio.output(17, False)
gpio.output(22, True)
while seconds > 0:
    if gpio.input(21) == 0:     
        gpio.output(17, False)
        gpio.output(22, False)
        seconds = -1
    seconds = seconds - 1
    time.sleep(0.5)

gpio.cleanup()
"""

while not(GPIO.input(lswitch_gpio27) and GPIO.input(lswitch_gpio22)): # While both limit switches are not pressed

    x=input('Enter "o" for open and "c" for close: ')    # asks for input and stores into x 

    if (x == "o"):      # if open
        GPIO.output(motor_in1, GPIO.HIGH)       # turns on motor opening
        GPIO.output(motor_in2, GPIO.LOW)        # turns off motor closing
        print("opening...")
    else:               # if close
        GPIO.output(motor_in1, GPIO.LOW)        # turns off motor opening
        GPIO.output(motor_in2, GPIO.HIGH)       # turns on motor closing
        print("closing...")

    print("starting motor")


# clean up turning off motors and clean up
GPIO.output(motor_in1, GPIO.LOW)        
GPIO.output(motor_in2, GPIO.LOW)
GPIO.cleanup()
