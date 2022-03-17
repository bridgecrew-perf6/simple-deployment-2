## DIY Exercise

### Download the OpenVINO docker container & run

```
docker run -it -v $HOME/<MODEL_DIR>:/<MODEL_DIR>/ openvino/ubuntu20_data_runtime:2021.4
```

### Download a sample video or point to RTSP stream

```
gst-launch-1.0 rtspsrc location="<RTSP URL FOR INPUT>" ! decodebin ! videoconvert ! gvadetect model=/<MODEL_DIR>/vehicle-detection-0200/FP16/vehicle-detection-0200.xml ! gvawatermark ! gvaclassify model=/<MODEL_DIR>/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml model-proc=/<MODEL_DIR>/vehicle-attributes-recognition-barrier-0039/vehicle-attributes-recognition-barrier-0039.json ! gvawatermark ! x264enc ! rtspclientsink location="<RTSP URL FOR OUTPUT>" protocols=tcp sync=false
```
