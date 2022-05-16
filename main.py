from xml.etree.ElementTree import Comment
from flask import Flask, render_template, request, url_for, redirect
import cv2 as cv2
from pylab import *
import mediapipe as mp
import keyboard
import results
from timer import *
import RPi.GPIO as GPIO #ONLY WORKS IN RPI
import datetime
from time import sleep
from crontab import CronTab #FOR CRON ONLY WORKS IN RPI

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
drawingModule = mp.solutions.drawing_utils
handsModule = mp.solutions.hands
app = Flask(__name__)
isTime = True


tipIds = [4, 8, 12, 16, 20]     # tip of all fingers from thumb to pinky
state = None
Gesture = None
wCam, hCam = 720, 640           # dimensions of camera
cap = cv2.VideoCapture(-1)

# def check_schedule_time_with_realtime() -> bool:
#     x = str(getTime())
#     print(x)
#     if x == str(openTimer()):
#         return True
#     if x == str(closeTimer()):
#         return True
#     return False

#to define finger position as well as setting up for hand gestures
def fingerPosition(image, handNo=0) -> list:
    lmList = []
    with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
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

#to configure Crontab in Pi OS
def cronConfig(x,y):
    cron = CronTab(user='pi')
    job = cron.new(command='python3 motor.py', comment='turn on motor.py')
    job.setall(x, y, None, None, None)
    cron.write()

class ChiCurtain:

    #initialization of Pi IO ports
    def __init__(self):
        isMoving = False
        self.ground = 6
        self.motor_in1 = 23
        self.motor_in2 = 24
        self.motor_enA = 25
        self.lswitch_gpio27 = 13
        self.lswitch_gpio22 = 15
        self.driver_gpio23 = 16
        self.driver_gpio24 = 18
        self.voltage5 = 2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_in1, GPIO.OUT)
        GPIO.setup(self.motor_in2, GPIO.OUT)
        GPIO.setup(self.motor_enA, GPIO.OUT)
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.LOW)
   
    def openCurtain(self):
        GPIO.output(self.motor_in1, GPIO.HIGH)
        GPIO.output(self.motor_in2, GPIO.LOW)
        print("Starting...")

    def closeCurtain(self):
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.HIGH)
        print("Reversing...")

    def stopCurtain(self):
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.LOW)
        print("Stop")

#route for homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#route to set open Timer
@app.route('/openTimer', methods=['GET', 'POST'])
def openTimer():
    data = request.form['appt']
    data_split = data.split(':')
    return redirect(url_for('timerCheck', x=data_split[0], y=data_split[1])) #redirects to route /timerCheck/x/y

#route to set Close timer
@app.route('/closeTimer', methods=['GET', 'POST'])
def closeTimer():
    data = request.form['appt2']
    data_split = data.split(':')
    return redirect(url_for('timerCheck', x=data_split[0], y=data_split[1])) #redirects to route /timerCheck/x/y

#route to set timer to Raspberry Pi
@app.route('/timerCheck/<x>/<y>')
def timerCheck(x,y):
    cronConfig(x,y)
    return("success")

#route for open button   
@app.route('/open', methods=['GET', 'POST'])
def home():
    print("hello from open")
    return ("hi")

#route for close button
@app.route('/close', methods=['GET', 'POST'])
def close_manual():
    print("hello from close")
    return ("hi")

#route for video capturing and hand gestures
@app.route('/capture', methods=['GET', 'POST'])
def capture():     
    state = ""
    cap.set(3, wCam)
    cap.set(4, hCam)
    with mp_hands.Hands(
        min_detection_confidence=0.8,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():           # all occurs when the capture button is pressed for now
            ret, frame = cap.read()     # taking many static picture with camera each time 
                                        # iterated through with while loop

            results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))     # converting BGR to RBG
            success, image = cap.read() 

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
                    drawingModule.draw_landmarks(frame, hand_landmarks, handsModule.HAND_CONNECTIONS)
            cv2.imshow('Test hand', frame)
            '''
            if cv2.waitKey(1) == 27:                # supposed to stop when ESC is pressed but doesn't work
                print("ESC key pressed exiting")    # prob will delete this if statement
                break
            '''
            lmList = fingerPosition(image)
            #print(lmList)
            if len(lmList) != 0:
                fingers = []                        # num of fingers up

                #thumb
                if(lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]):
                    fingers.append(1)               # add one if tip id is stretched further than that of inner nodes
                else:
                    fingers.append(0)

                #all other 4 fingers
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append(1)           # add one if tip id is stretched further than that of inner nodes
                    if (lmList[tipIds[id]][2] > lmList[tipIds[id] - 2][2] ):
                        fingers.append(0)

                totalFingers = fingers.count(1)
                print(totalFingers)
                #print(lmList[9][2])
                if totalFingers == 5:
                    state = "Play"
                    print("OPENING CURTAIN")
                    #break
                # fingers.append(1)
                if totalFingers == 0 and state == "Play":
                    state = "Pause"
                    print("CLOSING CURTAIN")
                    #break     
                           
    return ("hi")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

