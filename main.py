from xml.etree.ElementTree import Comment
from flask import Flask, render_template, request, url_for, redirect
import cv2 as cv2
import mediapipe as mp
import RPi.GPIO as GPIO  # ONLY WORKS IN RPI
import datetime
from time import sleep
from crontab import CronTab  # FOR CRON ONLY WORKS IN RPI
import threading

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
drawingModule = mp.solutions.drawing_utils
handsModule = mp.solutions.hands
app = Flask(__name__)
isTime = True


tipIds = [4, 8, 12, 16, 20]     # tip of all fingers from thumb to pinky
state = None
Gesture = None
wCam, hCam = 640, 480          # dimensions of camera

# to define finger position as well as setting up for hand gestures


def fingerPosition(image, cap, handNo=0) -> list:
    lmList = []
    with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:
        ret, frame = cap.read()
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
    return lmList

# to configure Crontab in Pi OS


def cronConfig(x, y, z):
    cron = CronTab(user='pi')
    if (z == 'open'):
        job = cron.new(
            command='python /home/pi/local/Xclass-Project/open.py', comment='turn on motor.py')
    else:
        job = cron.new(
            command='python /home/pi/local/Xclass-Project/close.py', comment='turn on motor.py')
    job.setall(y, x, None, None, None)
    cron.write_to_user(user=True)


class automated_curtain:

    def __init__(self):  # initialization of Pi IO ports
        isMoving = False
        self.ground = 6
        self.motor_in1 = 23
        self.motor_in2 = 24
        self.motor_enA = 25
        self.lswitch = 22
        self.rswitch = 27
        self.voltage5 = 2

        # Limit switch setup

    def openCurtain(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_in1, GPIO.OUT)
        GPIO.setup(self.motor_in2, GPIO.OUT)
        GPIO.setup(self.motor_enA, GPIO.OUT)
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.LOW)
        pwr = GPIO.PWM(self.motor_enA, 250)
        pwr.start(25)
        GPIO.setup(self.rswitch, GPIO.IN)
        GPIO.setup(self.lswitch, GPIO.IN)
        GPIO.setup(self.voltage5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print(self.ground, self.motor_in1, self.motor_in2, self.motor_enA)

        lswitch_pressed = not (GPIO.input(self.lswitch))
        rswitch_pressed = not (GPIO.input(self.rswitch))
        while (lswitch_pressed or (not lswitch_pressed and not rswitch_pressed)):
            lswitch_pressed = not (GPIO.input(self.lswitch))
            rswitch_pressed = not (GPIO.input(self.rswitch))
            GPIO.output(self.motor_in1, GPIO.LOW)
            GPIO.output(self.motor_in2, GPIO.HIGH)
            print("Starting...")

    def closeCurtain(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_in1, GPIO.OUT)
        GPIO.setup(self.motor_in2, GPIO.OUT)
        GPIO.setup(self.motor_enA, GPIO.OUT)
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.LOW)
        pwr = GPIO.PWM(self.motor_enA, 250)
        pwr.start(25)
        GPIO.setup(self.rswitch, GPIO.IN)
        GPIO.setup(self.lswitch, GPIO.IN)
        GPIO.setup(self.voltage5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        lswitch_pressed = not (GPIO.input(self.lswitch))
        rswitch_pressed = not (GPIO.input(self.rswitch))
        while (rswitch_pressed or (not lswitch_pressed and not rswitch_pressed)):
            lswitch_pressed = not (GPIO.input(self.lswitch))
            rswitch_pressed = not (GPIO.input(self.rswitch))
            GPIO.output(self.motor_in1, GPIO.HIGH)
            GPIO.output(self.motor_in2, GPIO.LOW)
            print("Reversing...")

    def stopCurtain(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_in1, GPIO.OUT)
        GPIO.setup(self.motor_in2, GPIO.OUT)
        GPIO.setup(self.motor_enA, GPIO.OUT)
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.LOW)
        pwr = GPIO.PWM(self.motor_enA, 1000)
        pwr.start(25)
        GPIO.setup(self.rswitch, GPIO.IN)
        GPIO.setup(self.lswitch, GPIO.IN)
        GPIO.setup(self.voltage5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.LOW)
        print("Stop")


# uncomment if doesn't work and delete first line in main fucntion
curtain = automated_curtain()

# route for homepage


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# route to set open Timer


@app.route('/openTimer', methods=['GET', 'POST'])
def openTimer():
    data = request.form['appt']
    data_split = data.split(':')
    # redirects to route /timerCheck/x/y
    return redirect(url_for('timerCheck', x=data_split[0], y=data_split[1], z='open'))

# route to set Close timer


@app.route('/closeTimer', methods=['GET', 'POST'])
def closeTimer():
    data = request.form['appt2']
    data_split = data.split(':')
    # redirects to route /timerCheck/x/y
    return redirect(url_for('timerCheck', x=data_split[0], y=data_split[1], z='close'))

# route to set timer to Raspberry Pi


@app.route('/timerCheck/<x>/<y>/<z>')
def timerCheck(x, y, z):
    cronConfig(x, y, z)
    return ("success")

# route for open button


@app.route('/open', methods=['GET', 'POST'])
def home():
    print("hello from open")
    curtain.openCurtain()
    return ("hi")

# route for close button


@app.route('/close', methods=['GET', 'POST'])
def close_manual():
    print("hello from close")
    curtain.closeCurtain()
    return ("hi")


def capture_gesture():
    cap = cv2.VideoCapture(0)
    print("Capture says hi")
    state = ""
    cap.set(3, wCam)
    cap.set(4, hCam)
    with mp_hands.Hands(
            min_detection_confidence=0.8,
            min_tracking_confidence=0.5) as hands:
        while cap.isOpened():           # all occurs when the capture button is pressed for now    # taking many static picture with camera each time

            ret, frame = cap.read()
            # iterated through with while l
            success, image = cap.read()
            cv2.waitKey(1)
            if not success:
                print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    drawingModule.draw_landmarks(
                        frame, hand_landmarks, handsModule.HAND_CONNECTIONS)
            cv2.imshow('Test hand', frame)

            lmList = fingerPosition(image, cap)
            if len(lmList) != 0:
                fingers = []                        # num of fingers up

                # thumb
                if (lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]):
                    # add one if tip id is stretched further than that of inner nodes
                    fingers.append(1)
                else:
                    fingers.append(0)

                # all other 4 fingers
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        # add one if tip id is stretched further than that of inner nodes
                        fingers.append(1)
                    if (lmList[tipIds[id]][2] > lmList[tipIds[id] - 2][2]):
                        fingers.append(0)

                totalFingers = fingers.count(1)
                print(totalFingers)
                if totalFingers == 5:
                    state = "Play"
                    print("OPENING CURTAIN")
                    curtain.openCurtain()
                if totalFingers == 0 and state == "Play":
                    state = "Pause"
                    print("CLOSING CURTAIN")
                    curtain.closeCurtain()


if __name__ == "__main__":
    capture_thread = threading.Thread(target=capture_gesture)
    capture_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
