import os
from flask import Flask, render_template, Response
import cv2
import numpy as np
import subprocess

app = Flask(__name__)

font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize and start realtime video capture
camera = cv2.VideoCapture(0)
camera.set(3, 640)  # set video widht
camera.set(4, 480)  # set video height

minW = 0.1*camera.get(3)
minH = 0.1*camera.get(4)


def gen_frames():
    while True:
        succes, frame = camera.read()
        subprocess.run(['python', 'detect.py', '--source', '0'], shell=True)
        if not succes:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/video_feed')
def video_feed():
	return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
	app.run(debug=True)