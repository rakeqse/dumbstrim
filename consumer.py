import datetime
import cv2
import numpy as np
from flask import Flask, Response, render_template
from kafka import KafkaConsumer

topic='simple-strim'

consumer=KafkaConsumer(topic, bootstrap_servers=['violpi:9092'])

face_cascade=cv2.CascadeClassifier()
face_cascade.load(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

eye_cascade=cv2.CascadeClassifier()
eye_cascade.load(cv2.data.haarcascades + "haarcascade_eye.xml")

def detectface(frame):
    gray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)

    for (x,y,w,h) in faces:
        center= (x+w//2,y+h//2)
        frame=cv2.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)

        faceROI=gray[y:y+h,x:x+w]
        eyes=eye_cascade.detectMultiScale(faceROI)
        
        for (x2, y2, w2, h2) in eyes:
            eye_center=(x+x2+w2//2, y+y2+h2//2)
            radius=int(round((w2+h2)*0.25))
            frame=cv2.circle(frame, eye_center, radius, (255, 0, 0), 4)
    return frame

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video', methods=['GET'])
def video():
    return Response(getVideoStream(), mimetype='multipart/x-mixed-replace; boundary=frame')

def decodeNp(data):
    nparr = np.frombuffer(data, dtype=np.uint8)
    img=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    frame=detectface(img)
    ret, jpg= cv2.imencode('.jpg', frame)
    return jpg.tobytes()


def getVideoStream():
    for msg in consumer:

        val=decodeNp(msg.value)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n'+ val + b'\r\n\r\n')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
