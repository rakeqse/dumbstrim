import sys
import time
import cv2
import numpy as np
from kafka import KafkaProducer

topic='simple-strim'

def publish_cam():
    
    producer = KafkaProducer(bootstrap_servers='violpi:9092')

    cam = cv2.VideoCapture(0)

    try:
        while(True):
            success, frame = cam.read()

            # turn to grayscale
            # gray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.resize(frame, [640, 480])

            # encode into jpg
            ret, buffer=cv2.imencode('.jpg', frame)

            producer.send(topic, buffer.tobytes())

    except:
        print("\nExiting.")
        sys.exit(1)
    cam.release()

if __name__ == "__main__":
    print("publishing feed...")
    publish_cam()




