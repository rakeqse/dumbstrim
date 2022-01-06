import cv2 as cv
import numpy as np

face_cascade = cv.CascadeClassifier()

face_cascade.load(cv.data.haarcascades +
                  "haarcascade_frontalface_default.xml")

eye_cascade = cv.CascadeClassifier()
eye_cascade.load(cv.data.haarcascades + "haarcascade_eye.xml")


def detectface(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        center = (x+w//2, y+h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2),
                           0, 0, 360, (255, 0, 255), 4)

        faceROI = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(faceROI)

        for (x2, y2, w2, h2) in eyes:
            eye_center = (x+x2+w2//2, y+y2+h2//2)
            radius = int(round((w2+h2)*0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0), 4)
    return frame
