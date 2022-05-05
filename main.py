from flask import Flask, render_template, request, url_for, redirect
import cv2 as cv2
from pylab import *
import mediapipe as mp
#import keyboard

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
app = Flask(__name__)

tipIds = [4, 8, 12, 16, 20]
state = None
Gesture = None
wCam, hCam = 720, 640

def fingerPosition(image, handNo=0):
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            # print(id,lm)
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
    return lmList

@app.route('/', methods=['GET', 'POST'])
def index():
    print("hi")
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form['appt']
    return (data)

@app.route('/open', methods=['GET', 'POST'])
def home():
    print("hello from open")
    return ("hi")

@app.route('/capture', methods=['GET', 'POST'])
def capture():     
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    with mp_hands.Hands(
        min_detection_confidence=0.8,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
                continue
            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lmList = fingerPosition(image)
            #print(lmList)
            if len(lmList) != 0:
                fingers = []
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append(1)
                    if (lmList[tipIds[id]][2] > lmList[tipIds[id] - 2][2] ):
                        fingers.append(0)
                totalFingers = fingers.count(1)
                print(totalFingers)
                #print(lmList[9][2])
                if totalFingers == 5:
                    state = "Play"
                    print("OPENING CURTAIN")
                    break
                # fingers.append(1)
                if totalFingers == 0 and state == "Play":
                    state = "Pause"
                    print("CLOSING CURTAIN")
                    break            
                #if keyboard.read_key() == "q":
                #    print("You pressed q")
                #    break           # if the `q` key was pressed, break from the loop

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)

