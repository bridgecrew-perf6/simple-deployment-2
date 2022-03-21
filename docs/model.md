# Distribution Matching for Crowd Counting (DM-Count)

The model used on this reference implementation is Distribution Matching for Crowd Counting (DM-Count) model to predict crowd density map.

The paper for the model can be found [here](https://arxiv.org/pdf/2009.13077.pdf)

We use the DM-Count model trained on [UCF-QNRF dataset](https://www.crcv.ucf.edu/data/ucf-qnrf/). 

The pretrined model is donwloaded from [cvlab-stonybrook/DM-Count](https://github.com/cvlab-stonybrook/DM-Count) opensource repo.


## Model Conversion

The DM-Count pretrained model is available on pytorch. We converted the pytorch model to onnx and then converted to OpenVINO.

    Pytorch -> ONNX -> OpenVINO

### Conversion from Pytorch to ONNX

The following can be used as a reference to convert the DM-Count pytorch model to ONNX format. 

The model vgg19 imported on the below script from the [cvlab-stonybrook/DM-Count](https://github.com/cvlab-stonybrook/DM-Count) repo.


```python
import torch
from models import vgg19 

model_path = "<pretrained DM-Count Model pth file>"
onnx_model_path = "<converted ONNX model save path>"
device = torch.device("cpu")
inputs = torch.randn(1, 3, 512, 768, requires_grad=True)

# Initialize the DM-Count model
model = vgg19()

# load the model weight file to the device
model.load_state_dict(torch.load(model_path, device))

# export the pytorch model to ONNX
torch.onnx.export(
    model,  # model
    inputs,  # model input
    onnx_model_path,  # where to save the model
    export_params=True,  # store the trained parameter weights inside the model file
    opset_version=12,  # the ONNX version to export the model to
    do_constant_folding=True,  # whether to execute constant folding for optimization
    input_names=["input"],  # the model's input names
    output_names=["output"],  # the model's output names
    )
```


### Converting ONNX model to OpenVINO

The following command is used to convert the ONNX model to OpenVINO.


```sh
python3 mo_onnx.py --input_model /home/ubuntu/dm_count.onnx --mean_value [123.675,116.28,103.53] --scale_values [58.395,57.12,57.375] --output_dir /home/ubuntu/FP32  --data_type FP32
```

Note: The `--mean_value` and `--scale_values` as specific to the UCF-QNRF dataset the model is trained on.