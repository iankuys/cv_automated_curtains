import RPi.GPIO as GPIO

# must instsall RPi.GPIO see README.md under to set up


# take a look at this:
# https://github.com/vishytheswishy/junk-transporter-backend/blob/main/motor.py


import RPi.GPIO as GPIO    

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
# p=GPIO.PWM(en,1000)
p.start(25)

while True: 

# Opening curtain 
  # Gesture control --> motor starts
  # Timer --> motor starts

# When the curtain is extending and limit switch is hit --> motor stops
# When the curtain is retracting and limit switch is hit --> motor stops

# If disconnected break
