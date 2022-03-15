#!/usr/bin python3
# Copyright (C) 2021 Scaler.ai
"""
MQTT Subscriber script for receiving data from Video Analytics
Serving DL Streamer extension

version: 1.0
"""
import base64
import json
import logging
import os
from json import JSONDecodeError
from logging import Logger

import cv2
import numpy as np
import paho.mqtt.client as mqtt


class MQTTSub:
    """MQTTSub class to subscribe to crowd MQTT topic"""
    def __init__(self, host_ip: str, is_print: bool):
        """Initialize MQTTSub class"""
        self.host_ip = host_ip
        self.stream_data = {
            100: {
                'count': 0,
                'fps': 0,
                'density': np.zeros((64, 96, 3), dtype=np.uint8),
                'live': np.zeros((64, 96, 3), dtype=np.uint8),
                'latitude': 0,
                'longitude': 0
            }
        }
        self.log = self.init_log()
        self.is_print = is_print
        self.connect()

    def init_log(self) -> Logger:
        """Create and Initialize logger

        :returns log: Logger object
        """
        log_format = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s : %(message)s",
            datefmt="%d/%m/%Y %I:%M:%S %p",
        )
        log = logging.getLogger('Crowd Telegraf')
        log.setLevel(logging.INFO)
        handler = logging.FileHandler(os.path.join("/tmp/crowd_telegraf.log"))
        handler.setFormatter(log_format)
        log.addHandler(handler)
        log.info("Log file created")

        return log

    def decode(self, encoded_img: str) -> np.ndarray:
        """
        Decode base64 encoded images received over mqtt

        :params encoded_img: base64 encoded image

        :returns img: decoded numpy array
        """
        img_original = base64.b64decode(encoded_img)
        img_as_np = np.frombuffer(img_original, dtype=np.uint8)
        img = cv2.imdecode(img_as_np, cv2.IMREAD_COLOR)

        return img

    def post_process(self, display: np.ndarray, model_out: np.ndarray) -> np.ndarray:
        """
        Create density map over the display image

        :param display: Original image
        :param model_out: Density map

        :returns added_image: Density mapped image
        """
        vis_img = np.squeeze(model_out.reshape(1, 1, 64, 96))
        vis_img = (vis_img - vis_img.min()) / (vis_img.max() - vis_img.min() + 1e-5)
        vis_img = (vis_img * 255).astype(np.uint8)
        vis_img = cv2.applyColorMap(vis_img, cv2.COLORMAP_JET)
        vis_img = cv2.resize(
            vis_img, (display.shape[1], display.shape[0]),  cv2.INTER_AREA
        )
        added_image = cv2.addWeighted(display, 1, vis_img, 0.4, 0)

        return added_image

    def on_message(self, client, userdata, msg) -> None:
        """MQTT on_message method"""
        try:
            payload_data = json.loads(msg.payload)
        except JSONDecodeError:
            error_msg = ("Error loading MQTT payload received. Plugin will ",
                         "reload in 20 seconds.")
            self.log.error(error_msg)
            exit(1)

        try:
            stream = payload_data['stream']
            if self.is_print:
                count = payload_data['count']
                fps = payload_data['fps']
                latitude = payload_data['latitude']
                longitude = payload_data['longitude']

                self.stream_data = {
                    stream: {
                        'count': count,
                        'fps': fps,
                        'latitude': latitude,
                        'longitude': longitude
                    }
                }
            else:
                org_img = payload_data['image']
                model_out = np.asarray(payload_data['density'], dtype=np.float32)
        except KeyError:
            error_msg = ("Error loading image/count details from payload. ",
                         "Plugin will reload in 20 seconds")
            self.log.error(error_msg)
            exit(1)

        if not self.is_print:
            try:
                live = self.decode(org_img)
            except Exception as exc:
                error_msg = f"{type(exc).__name__}: {exc}"
                self.log.erro(error_msg)
                exit(1)

            density = self.post_process(live, model_out)

            self.stream_data = {
                stream: {
                    'density': density,
                    'live': live
                }
            }

    def connect(self) -> None:
        """Connect to MQTT Server and run loop in seperate thread"""
        client = mqtt.Client()
        try:
            client.connect(self.host_ip)
        except Exception as exc:
            error_msg = ("Error connectint to MQTT Server. \n"
                         f"{type(exc).__name__}: {exc}")
            self.log.error(error_msg)
            exit(1)

        client.subscribe("crowd")
        client.on_message = self.on_message
        self.log.info("Connected to MQTT Server successfully.")
        # start client loop in seperate thread
        client.loop_start()
