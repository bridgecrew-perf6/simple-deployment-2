#!/bin/bash

GST_PLUGIN_PATH=${GST_PLUGIN_PATH}:/usr/lib/x86_64-linux-gnu/gstreamer-1.0


# this one below is working
gst-launch-1.0 filesrc location="../../../input/stream1.mkv" ! decodebin ! videoconvert ! video/x-raw,format=BGRx ! gvainference model=../../../model/dm_count/1/FP32/dm_count.xml name=crowd model-instance-id=model0 inference-interval=5 ! videoconvert ! avimux ! filesink location="foo.avi" -e
