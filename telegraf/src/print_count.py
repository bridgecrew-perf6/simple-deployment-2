#!/usr/bin python3
# Copyright (C) 2021 Scaler.ai
"""
Image server based on flask to serve crowd density images with telegraf

version: 1.0
"""
import os
import time

from mqtt_sub import MQTTSub
import uuid

def print_count() -> None:

    """Print crowd count by reading data from MQTTSub class"""
    MQTT_IP = os.environ['MQTT_IP']
    mqtt = MQTTSub(MQTT_IP, True)

    while True:
        current_time = int(time.time())
        stream_data = mqtt.stream_data
        stream = next(iter(stream_data.keys()))

        line = ("crowd,stream={} count={},fps={},latitude={},longitude={}"
                " {} \n").format(
                                stream, stream_data[stream]['count'],
                                stream_data[stream]['fps'],
                                stream_data[stream]['latitude'],
                                stream_data[stream]['longitude'],
                                current_time
                            )
        print(line)
        time.sleep(0.001)


if __name__ == "__main__":
    print_count()
