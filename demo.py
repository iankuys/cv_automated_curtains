from xml.etree.ElementTree import Comment
from flask import Flask, render_template, request, url_for, redirect
import cv2 as cv2
import mediapipe as mp
import datetime
from time import sleep
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

def capture_gesture():
    cap = cv2.VideoCapture(0)
    print("Capture says hi")
    state = ""
    cap.set(3, wCam)
    cap.set(4, hCam)
    with mp_hands.Hands(
            min_detection_confidence=0.8,
            min_tracking_confidence=0.5) as hands:
        print("hi again")
        print(cap.isOpened())
        while cap.isOpened():           # all occurs when the capture button is pressed for now    # taking many static picture with camera each time

            print("Camera is Ready")
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
                if totalFingers == 0:
                    state = "Pause"
                    print("Stopping Application")
                    break
                    
if __name__ == "__main__":
    
    capture_thread = threading.Thread(target=capture_gesture)
    capture_thread.start()
    capture_thread.join()