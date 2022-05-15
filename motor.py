import RPi.GPIO as GPIO

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
GPIO.setup(lswitch_gpio27, GPIO.IN) # in or out
GPIO.setup(lswitch_gpio22, GPIO.IN) # in or out
GPIO.setup(voltage5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Working Motor and Limit Switches
def josh_function():
    print("switch 1 state:", GPIO.input(lswitch_gpio27))
    print("switch 2 state:", GPIO.input(lswitch_gpio22))

    while True:
        if state == "o":
            GPIO.output(motor_in1, GPIO.HIGH)       
            GPIO.output(motor_in2, GPIO.LOW)        
            print("opening curtain...")
        elif state == "c":
            GPIO.output(motor_in1, GPIO.LOW)       
            GPIO.output(motor_in2, GPIO.HIGH)
            print("closing curtain...")

        if not GPIO.input(lswitch_gpio27) or not GPIO.input(lswitch_gpio22):
            GPIO.output(motor_in1, GPIO.LOW)       
            GPIO.output(motor_in2, GPIO.LOW)
            break


while True:
    state = input('Enter "o" for open and "c" for close: ') 
    if (state == "o" and not(GPIO.input(lswitch_gpio27))) or (state == "c" and not(GPIO.input(lswitch_gpio22))):
        josh_function()

GPIO.cleanup()