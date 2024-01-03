import RPi.GPIO as GPIO


GPIO.cleanup()


def openCurtain():

    ground = 6
    motor_in1 = 23
    motor_in2 = 24
    motor_enA = 25
    lswitch = 22
    rswitch = 27
    voltage5 = 2

    # motor setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_in1, GPIO.OUT)
    GPIO.setup(motor_in2, GPIO.OUT)
    GPIO.setup(motor_enA, GPIO.OUT)
    GPIO.output(motor_in1, GPIO.LOW)
    GPIO.output(motor_in2, GPIO.LOW)

    pwr = GPIO.PWM(motor_enA, 500)
    pwr.start(25)

    # limit switch setup
    GPIO.setup(rswitch, GPIO.IN)
    GPIO.setup(lswitch, GPIO.IN)
    GPIO.setup(voltage5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # opening curtain
    lswitch_pressed = not (GPIO.input(lswitch))
    rswitch_pressed = not (GPIO.input(rswitch))
    while (lswitch_pressed or (not lswitch_pressed and not rswitch_pressed)):
        lswitch_pressed = not (GPIO.input(lswitch))
        rswitch_pressed = not (GPIO.input(rswitch))
        GPIO.output(motor_in1, GPIO.HIGH)
        GPIO.output(motor_in2, GPIO.LOW)
        print("Opening Curtain...")


openCurtain()
