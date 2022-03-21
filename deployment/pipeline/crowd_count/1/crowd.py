#!/usr/bin python3
# Copyright (C) 2021 scalers.ai
"""
gvapython script for crowd pipeline on Video Analytics Serving
DL Streamer extension

version: 2.0
"""
import base64
import json
import sys
import time

import cv2
import numpy as np

from gstgva import VideoFrame



class InferenceTime:
    """
    Class to add the inference start time to frame messages
    """
    def process_frame(self, frame: VideoFrame):
        """
        method to store the model inference start time

        :param frame: gstgva.VideoFrame object

        :returns bool
        """
        for message in frame.messages():
            ext_msg = json.loads(message)
            ext_msg['time'] = str(time.time_ns())
            frame.add_message(json.dumps(ext_msg))

        return True


class CrowdCount:
    """Crowd Counting class for DM-Count Model"""

    # the stream id will be used to identify the stream
    def __init__(self, stream: str, latitude: str, longitude: str, ) -> None:
        self.stream = stream
        self.latitude = latitude
        self.longitude = longitude

    def process_frame(self, frame: VideoFrame) -> bool:
        """
        gvapython script for post processing operation for the
        DM-Count crowd density model

        :param frame: gstgva.VideoFrame object

        :returns bool
        """

        # calculate model fps by getting inference start time
        data = json.loads(frame.messages()[1])['time']
        inference_time = time.time_ns() - int(data)
        fps = 1000000000 / inference_time

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
                # formatting metadata to send it through MQTT
                payload = {
                    "density": tensor.data().tolist(),
                    "count": str(int(count)),
                    "stream": str(self.stream),
                    "fps": fps,
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
        return True
