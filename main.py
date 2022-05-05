from flask import Flask, render_template, request, url_for, redirect
import cv2 as cv
from pylab import *
import mediapipe as mp
app = Flask(__name__)

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
    cam_port = 0
    cam = cv.VideoCapture(cam_port)
    result, image = cam.read()
    if result:
        cv.imwrite("filename.png", image)
    else:
        print("No image detected. Please! try again")

    return ("hi")
    # figure out how to send image to another server (post request)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)