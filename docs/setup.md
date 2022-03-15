# Setting up IoT Edge Device

## 1. Setting up Docker on Edge device

To setup docker on Edge device, follow the document [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/) by Docker.

## 2. Setting up Azure IoT Edge on the Edge device

To install and setup Azure IoT Edge on a Linux Edge device, follow the document [Create and provision an IoT Edge device on Linux using symmetric keys](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-provision-single-device-linux-symmetric?view=iotedge-2020-11&tabs=azure-portal) by microsoft.

*Note: Skip the step [Install a container engine](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-provision-single-device-linux-symmetric?view=iotedge-2020-11&tabs=azure-portal#install-a-container-engine) on the above mentioned setup document. We will be using the `docker-engine` as the container engine instead of `moby-engine`*

Once the Azure IoT Edge is installed on the Edge device, follow the below steps.

1. Update the permissions the crowd demo videos to user `localedgeuser` (user id 1010) and group `localedgegroup` (group id 1010)

    ```sh
    sudo chown 1010:1010 crowd_stream1.mkv
    sudo chown 1010:1010 crowd_stream2.mkv
    ```

2. Copy the crowd demo videos to the directory `/home/localedgeuser/samples/input`.
    
    ```
    sudo cp crowd_stream1.mkv /home/localedgeuser/samples/input

    sudo cp crowd_stream2.mkv /home/localedgeuser/samples/input
    ```
