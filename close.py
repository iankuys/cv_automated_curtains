import RPi.GPIO as GPIO

GPIO.cleanup()

def closeCurtain():
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

    pwr = GPIO.PWM(motor_enA, 500)
    pwr.start(25)

    # Limit Switch Setup
    GPIO.setup(rswitch, GPIO.IN)
    GPIO.setup(lswitch, GPIO.IN)
    GPIO.setup(voltage5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Closing Motor
    lswitch_pressed = not (GPIO.input(lswitch))
    rswitch_pressed = not (GPIO.input(rswitch))
    while (rswitch_pressed) or (not lswitch_pressed and not rswitch_pressed):
        lswitch_pressed = not (GPIO.input(lswitch))
        rswitch_pressed = not (GPIO.input(rswitch))
        GPIO.output(motor_in1, GPIO.LOW)
        GPIO.output(motor_in2, GPIO.HIGH)
        print("Closing curtain...")


closeCurtain()
