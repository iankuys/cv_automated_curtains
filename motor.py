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
    print("switch 1 state:", lswitch1_pressed)
    print("switch 2 state:", lswitch2_pressed)

    while True:
        if state == "o":
            GPIO.output(motor_in1, GPIO.HIGH)       
            GPIO.output(motor_in2, GPIO.LOW)
            print("opening curtain...")
        elif state == "c":
            GPIO.output(motor_in1, GPIO.LOW)       
            GPIO.output(motor_in2, GPIO.HIGH)
            print("closing curtain...")
        if lswitch1_pressed or not lswitch2_pressed:
            GPIO.output(motor_in1, GPIO.LOW)       
            GPIO.output(motor_in2, GPIO.LOW)
            break



if __name__ == "__main__":
    lswitch1_pressed = not(GPIO.input(lswitch_gpio27))
    lswitch2_pressed = not(GPIO.input(lswitch_gpio22))
    while True:
        state = input('Enter "o" for open and "c" for close: ') 
        # if (state == "c") and (lswitch1_pressed): # Curtain open switch is 
        #     pass
        # elif (state == "o") and (lswitch2_pressed):
        #     pass
        # elif (state == "o"):
        #     GPIO.output(motor_in1, GPIO.HIGH)       
        #     GPIO.output(motor_in2, GPIO.LOW)
        #     josh_function(state)
        # elif (state == "c"):
        #     GPIO.output(motor_in1, GPIO.LOW)       
        #     GPIO.output(motor_in2, GPIO.HIGH)
        josh_function()

    GPIO.cleanup()