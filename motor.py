import RPi.GPIO as GPIO
import time

# must instsall RPi.GPIO see README.md under to set up

GPIO.cleanup()
# take a look at this:
# https://github.com/vishytheswishy/junk-transporter-backend/blob/main/motor.py
ground = 6
motor_in1 = 23
motor_in2 = 24
motor_enA = 25
lswitch_gpio27 = 13
lswitch_gpio22 = 15
driver_gpio23 = 16
driver_gpio24 = 18
voltage5 = 2

# Motor Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_in1, GPIO.OUT)
GPIO.setup(motor_in2, GPIO.OUT)
GPIO.setup(motor_enA, GPIO.OUT)
GPIO.output(motor_in1, GPIO.LOW)
GPIO.output(motor_in2, GPIO.LOW)
p=GPIO.PWM(motor_enA, 1000)

p.start(25)

# Limit Switch Setup
GPIO.setup(lswitch_gpio27, GPIO.OUT)
GPIO.setup(lswitch_gpio22, GPIO.OUT)
GPIO.setup(voltage5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# seconds = 10
# print "reverse"
# gpio.output(17, False)
# gpio.output(22, True)
# while seconds > 0:
#     if gpio.input(21) == 0:     
#         gpio.output(17, False)
#         gpio.output(22, False)
#         seconds = -1
#     seconds = seconds - 1
#     time.sleep(0.5)
# gpio.cleanup()

def startMotor():

  print("starting motor")

def openCurtain():
  pass
  # stop when limit switch hit

def closeCurtain():
  pass
  # stop when limit switch hit

while(1):

    x=input("What mode")
    s="s"

    if (x == s):
        GPIO.output(motor_in1, GPIO.HIGH)
        GPIO.output(motor_in2, GPIO.LOW)
        print("Starting...")

    else:
        GPIO.output(motor_in1, GPIO.LOW)
        GPIO.output(motor_in2, GPIO.HIGH)
        print("Reversing...")

    print("starting motor")


# Opening curtain 
  # Gesture control --> motor starts
  # Timer --> motor starts

# When the curtain is extending and limit switch is hit --> motor stops
# When the curtain is retracting and limit switch is hit --> motor stops

# If disconnected break
