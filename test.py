import numpy as np
import cv2 as cv
from kafka import KafkaConsumer, TopicPartition
from decode import detectface
from consumer import decodeNp

topic = 'multi-stream'

consumer = KafkaConsumer(bootstrap_servers=['violpi:9092'], )
consumer.assign([TopicPartition(topic, 1)])


def decodeNp(data):
    nparr = np.frombuffer(data, dtype=np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)
    frame = detectface(img)
    return frame


for message in consumer:
    frame = decodeNp(message.value)
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

# Release everything if job is finished
cv.destroyAllWindows()
