import datetime

from flask import Flask, Response, render_template
from kafka import KafkaConsumer

topic='simple-strim'

consumer=KafkaConsumer(topic, bootstrap_servers=['violpi:9092'])

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video', methods=['GET'])
def video():
    return Response(getVideoStream(), mimetype='multipart/x-mixed-replace; boundary=frame')

def getVideoStream():
    for msg in consumer:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n'+ msg.value + b'\r\n\r\n')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
