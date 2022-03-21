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
from azure.iot.device import IoTHubModuleClient, Message

module_client = IoTHubModuleClient.create_from_edge_environment()

# Connect the client.
module_client.connect()

ALERT_INTERVAL = 10
ALERT_THRESOLD = 250
ALERT_OFFSET_TIME = time.time()

def send_alert_ava(message, output):
    msg = Message(message)
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"
    msg.custom_properties["crowd-density-warning"] = "yes"
    module_client.send_message_to_output(msg, output)

def print_count() -> None:
    global ALERT_OFFSET_TIME
    """Print crowd count by reading data from MQTTSub class"""
    MQTT_IP = os.environ['MQTT_IP']
    mqtt = MQTTSub(MQTT_IP, True)

    while True:
        current_time = int(time.time() * 1000000000)
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

        if ((int(stream_data[stream]['count'])>=ALERT_THRESOLD) and (time.time() - ALERT_OFFSET_TIME>=ALERT_INTERVAL)):
            ALERT_OFFSET_TIME=time.time()
            send_alert_ava(str(stream_data[stream]['count']), str(stream))


if __name__ == "__main__":
    print_count()
