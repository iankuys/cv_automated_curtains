import RPi.GPIO as GPIO
import time

# must instsall RPi.GPIO see README.md under to set up


# take a look at this:
# https://github.com/vishytheswishy/junk-transporter-backend/blob/main/motor.py

ground = 6
motor_in1 = 7
motor_in2 = 8
motor_enA = 25
lswitch_gpio27 = 13
lswitch_gpio22 = 15
driver_gpio23 = 16
driver_gpio24 = 18
voltage5 = 2

# Motor Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en_a,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

# Limit Switch Setup
# GPIO.setup(lswitch_gpio27, GPIO.OUT)
# GPIO.setup(lswitch_gpio22, GPIO.OUT)
# GPIO.setup(voltage5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
  pwr = GPIO.PWM(motor_enA,1000)
  pwr.start(25)

def openCurtain():
  pass
  # stop when limit switch hit

def closeCurtain():
  pass
  # stop when limit switch hit

startMotor()
while True:
  if (GPIO.input(lswitch_gpio27)) or (GPIO.input(lswitch_gpio22)):
    GPIO.cleanup()
  else:
    break
  
# Opening curtain 
  # Gesture control --> motor starts
  # Timer --> motor starts

# When the curtain is extending and limit switch is hit --> motor stops
# When the curtain is retracting and limit switch is hit --> motor stops

# If disconnected break
