# Crowd Analytics Solution Setup Guide

# Prerequisites
1. An edge machine with Ubuntu and iGPU.

# Setup
## Setting up deployment machine
Complete the following steps to setup the deployment machine.
1. [Install Docker](https://docs.docker.com/engine/install/ubuntu/)
    
2. Install Docker compose

    ```sh
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

    sudo chmod +x /usr/local/bin/docker-compose
    ```

## Set Model Precision and Target Hardware
### Setting model precision
The solution offers model with precisions **FP32, FP16** and **INT8**. To update the solution to run on any of these precision model, update the `.env` file parameter `PRECISION=<Model Precision>`.

eg, setting model precision to FP16

```sh
DEVICE=CPU
PRECISION=FP16
```

### Setting Target Hardware
The solution will run on CPU and iGPU. To swithc between the target hardwares, update the `.env` file parameter `DEVICE=<Target Device>`

eg, setting targte device as GPU
```sh
DEVICE=GPU
PRECISION=FP16
```

## Build and run solution

1. Follow the below steps to setup the edge deployment machine.

    ```sh
    sudo docker-compose build

    sudo docker-compose up
    ```


# Visualize Crowd Analytics Edge UI
Follow the below steps to visualize the results using Crowd Analytics Edge UI.

1. On your deployment machine, open the [`localhost:3000`](http://localhost:3000) to open the Grafana UI.
    > If you are accessing the UI from a different machine, forward the ports `3000` and `5100` to the machine.
2. Use the following credentials to login
    * Username: `admin`
    * Password: `admin`
3. Click on the **Search** icon on the left navbar and select **Crowd Analytics Edge UI v1**.