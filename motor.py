import RPi.GPIO as GPIO
import time

# must instsall RPi.GPIO see README.md under to set up

GPIO.cleanup()
# sets variables to input/output pins
# take a look at this:
# https://github.com/vishytheswishy/junk-transporter-backend/blob/main/motor.py
ground = 6
motor_in1 = 23
motor_in2 = 24
motor_enA = 25
lswitch = 22
rswitch = 27
voltage5 = 2

# Motor Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_in1, GPIO.OUT)
GPIO.setup(motor_in2, GPIO.OUT)
GPIO.setup(motor_enA, GPIO.OUT)
GPIO.output(motor_in1, GPIO.LOW)
GPIO.output(motor_in2, GPIO.LOW)

pwr = GPIO.PWM(motor_enA, 1000)
pwr.start(25)

# Limit Switch Setup
GPIO.setup(rswitch, GPIO.IN)
GPIO.setup(lswitch, GPIO.IN)
GPIO.setup(voltage5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Working Motor and Limit Switches
def move_motor(state):
    print("left switch state:", lswitch_pressed)
    print("right switch state:", rswitch_pressed)

    while True:
        if state == "o":
            GPIO.output(motor_in1, GPIO.HIGH)       
            GPIO.output(motor_in2, GPIO.LOW)
            print("opening curtain...")
        elif state == "c":
            GPIO.output(motor_in1, GPIO.LOW)       
            GPIO.output(motor_in2, GPIO.HIGH)
            print("closing curtain...")
        time.sleep(0.3) # Allows curtain to move even when limit switch starts pressed
        if lswitch_pressed or not rswitch_pressed:
            GPIO.output(motor_in1, GPIO.LOW)
            GPIO.output(motor_in2, GPIO.LOW)
            break

if __name__ == "__main__":
    lswitch_pressed = not(GPIO.input(lswitch))
    rswitch_pressed = not(GPIO.input(rswitch))
    while True:
        state = input('Enter "o" for open and "c" for close: ')
        if not lswitch_pressed and not rswitch_pressed:
            move_motor(state)
        elif (state == "c") and (rswitch_pressed):
            move_motor(state)
        elif (state == "o") and (lswitch_pressed):
            move_motor(state)
        else:
            pass # Cannot further open curtain if fully open or close if fully closed

    GPIO.cleanup()
