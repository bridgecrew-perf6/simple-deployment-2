# Copyright (C) 2022 scalers.ai

# #### Single Stream
runPipeline() {
gst-launch-1.0 \
    rtspsrc location=rtsp://rtspsim:8554/stream1.mkv ! decodebin  ! videoconvert ! video/x-raw,format=BGRx ! \
    gvainference model=model/dm_count/1/$PRECISION/dm_count.xml device=$DEVICE ! \
    gvapython module=crowd.py kwarg='{"stream": "100", "latitude": "-6.18188735639403", "longitude": "106.81674548492997"}' class=CrowdCount \
    fakesink sync=false

return 1
}

# #### Two Streams: To run two streams uncomment this code and comment Single Stream - runPipeline function.
# runPipeline() {
# gst-launch-1.0 \
#     rtspsrc location=rtsp://rtspsim:8554/stream1.mkv ! decodebin  ! videoconvert ! video/x-raw,format=BGRx ! \
#     gvainference model=model/dm_count/1/$PRECISION/dm_count.xml device=$DEVICE ! \
#     gvapython module=crowd.py kwarg='{"stream": "100", "latitude": "-6.18188735639403", "longitude": "106.81674548492997"}' class=CrowdCount \
#     fakesink sync=false \
#     rtspsrc location=rtsp://rtspsim:8554/stream2.mkv ! decodebin  ! videoconvert ! video/x-raw,format=BGRx ! \
#     gvainference model=model/dm_count/1/$PRECISION/dm_count.xml device=$DEVICE ! \
#     gvapython module=crowd.py kwarg='{"stream": "100", "latitude": "-6.18188735639403", "longitude": "106.81674548492997"}' class=CrowdCount \
#     fakesink sync=false
# return 1
# }

until runPipeline;
do
    echo 'Restarting pipeline'
    sleep 1
done