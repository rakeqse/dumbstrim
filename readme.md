# dumbstrim
> simple stupid strim

this repo is a demo for kafka's streaming capabilities with producers and consumers

[source](https://medium.com/@kevin.michael.horan/distributed-video-streaming-with-python-and-kafka-551de69fe1d)

## how it works (simple part)

```
producer.py --> kafka-server <== consumer.py
(opencv)       (strim-topic)     (flask-server)
```
- `producer.py` uses `opencv` to get webcam feed `publish` it to  `kafka-server` through kafka-client
-  `consumer.py` uses  `consumer` provided by `kafka-client` to subscribe to `kafka's topic` which pulls the image stream produced by `producer.py` then displays to flask route `/video`

## limitations (stupid part)

since `consumer.py` sends a  `multipart response` so **only one request to** `/video` can see the jpg stream.