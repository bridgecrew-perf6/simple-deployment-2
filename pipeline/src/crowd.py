#!/usr/bin python3
# Copyright (C) 2022 scalers.ai
"""
gvapython script for crowd pipeline on Video Analytics Serving
DL Streamer extension

version: 3.0
"""
import base64
import json
import sys
import time

import cv2
import gi
import numpy as np

gi.require_version('Gst', '1.0')
import paho.mqtt.client as mqtt
from gi.repository import GObject, Gst
from gstgva import VideoFrame

Gst.init(sys.argv)


class CrowdCount:
    """Crowd Counting class for DM-Count Model"""

    # the stream id will be used to identify the stream
    def __init__(self, stream: str, latitude: str, longitude: str, ) -> None:
        self.stream = stream
        self.latitude = latitude
        self.longitude = longitude
        self.client = self.connect_mqtt()
        self.start_time = time.time()
        self.frame_count = 0
        self.avg_fps = 0

    def connect_mqtt(self) -> mqtt.Client:
        """
        Connect to MQTT broker

        :returns mqtt.Client
        """
        client = mqtt.Client()
        client.connect("MQTTBroker", 1883, 60)
        return client

    def process_frame(self, frame: VideoFrame) -> bool:
        """
        gvapython script for post processing operation for the
        DM-Count crowd density model

        :param frame: gstgva.VideoFrame object

        :returns bool
        """
        # calculate average fps for every 10 seconds
        self.frame_count += 1
        curr_time = time.time() - self.start_time
        if curr_time > 10:
            self.avg_fps = self.frame_count/curr_time

        for tensor in frame.tensors():
            # DM-Count model output layer 'output' provides the density map
            if tensor.layer_name() == 'output' and not tensor.layer_name() == "100":
                # calculating density map by taking sum of
                # all elements in model output
                count = np.sum(tensor.data())

                # capturing input frame and resizing to 380*500
                # the resized frame will be encoded with base64
                with frame.data() as image:
                    width = 500
                    height = 380
                    resized_image = cv2.resize(
                        image, (width, height),
                        interpolation=cv2.INTER_AREA
                    )
                    _, buffer = cv2.imencode('.jpg', resized_image)
                    jpg_as_text = base64.b64encode(buffer).decode()

                # formatting metadata to send it through MQTT
                payload = {
                    "image": jpg_as_text,
                    "density": tensor.data().tolist(),
                    "count": str(int(count)),
                    "stream": str(self.stream),
                    "fps": self.avg_fps,
                    "latitude": str(self.latitude),
                    "longitude": str(self.longitude)
                }

                iot_data = {
                    "crowd_count": str(int(count)),
                    "stream": str(self.stream),
                    "latitude": str(self.latitude),
                    "longitude": str(self.longitude)
                }
                frame.add_region(10, 30, 40, 50, json.dumps(iot_data), int(count))
                self.client.publish("crowd", json.dumps(payload))

        return True
