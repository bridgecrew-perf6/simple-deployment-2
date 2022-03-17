# Copyright (C) 2021 scalers.ai

runPipeline() {
gst-launch-1.0 \
    rtspsrc location=rtsp://rtspsim:8554/stream1.mkv ! decodebin  ! videoconvert ! video/x-raw,format=BGRx ! \
    gvapython module=crowd.py class=InferenceTime ! \
    gvainference model=model/dm_count/1/FP32/dm_count.xml inference-interval=5 ! \
    gvapython module=crowd.py kwarg='{"stream": "100", "latitude": "-6.18188735639403", "longitude": "106.81674548492997"}' class=CrowdCount \
    rtspsrc location=rtsp://rtspsim:8554/stream2.mkv ! decodebin  ! videoconvert ! video/x-raw,format=BGRx ! \
    gvapython module=crowd.py class=InferenceTime ! \
    gvainference model=model/dm_count/1/FP32/dm_count.xml inference-interval=5 ! \
    gvapython module=crowd.py kwarg='{"stream": "101", "latitude": "-6.28182735639403", "longitude": "106.71670548492997"}' class=CrowdCount 

return 1
}

until runPipeline;
do
    echo 'Restarting pipeline'
    sleep 1
done