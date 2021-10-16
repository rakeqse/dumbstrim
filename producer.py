import sys
import time
import cv2
from kafka import KafkaProducer

topic='simple-strim'

def publish_cam():
    
    producer = KafkaProducer(bootstrap_servers='violpi:9092')

    cam = cv2.VideoCapture(0)

    try:
        while(True):
            success, frame = cam.read()
            
            ret, buffer=cv2.imencode('.jpg', frame)
            producer.send(topic, buffer.tobytes())

    except:
        print("\nExiting.")
        sys.exit(1)
    cam.release()

if __name__ == "__main__":
    print("publishing feed...")
    publish_cam()




