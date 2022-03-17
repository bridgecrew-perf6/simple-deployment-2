"""
Copyright (C) 2021 Scaler.ai
Image server based on flask to serve crowd density images with telegraf

version: 1.0
"""
import os
import time
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from os import devnull

import cv2
from flask import Flask, Response, request

from mqtt_sub import MQTTSub

app = Flask(__name__)
MQTT_IP = os.environ['MQTT_IP']
mqtt = MQTTSub(MQTT_IP, False)


@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)


def gen_density(stream_id):
    """Collect frame from MQTTSub and serve on video feed endpoint"""
    while True:
        try:
            time.sleep(0.01)
            density = mqtt.stream_data[stream_id]['density']
        except KeyError:
            mqtt.log.error("Stream ID not found")
            continue

        ret, buffer = cv2.imencode('.jpg', density)
        if ret:
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def gen_live(stream_id):
    while True:
        try:
            time.sleep(0.01)
            live = mqtt.stream_data[stream_id]['live']
        except KeyError:
            mqtt.log.error("Stream ID not found")
            continue

        ret, buffer = cv2.imencode('.jpg', live)
        if ret:
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# density map video feed
@app.route('/density')
def video_feed():
    stream_id = request.args.get('stream', default="100", type=str)
    return Response(gen_density(stream_id), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/feed')
def live_feed():
    stream_id = request.args.get('stream', default="100", type=str)
    return Response(gen_live(stream_id), mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
    try:
        mqtt.log.info("Starting Video feed server")
        app.run(host='0.0.0.0', port=5100, debug=True)
    except Exception as exc:
        error_msg = ("Exception while starting video feed server. "
                     f"{type(exc).__name__}: {exc}")
        mqtt.log.error(error_msg)


if __name__ == '__main__':
    with suppress_stdout_stderr():
        main()
