# Crowd Analytics Solution Setup Guide

# Prerequisites
1. An edge machine with Ubuntu.
2. Azure Account with active suscription. Follow [this documentation](https://azure.microsoft.com/en-us/free/
) for know more about Creating Azure Account.
> Note: This requires an Azure subscrption account with both the **Contributor** and the **User Access Administrator** to the resource group.

# Setup
## Setting up Development machine
Complete the following steps to setup the deployment machine.
1. [Install Docker](https://docs.docker.com/engine/install/ubuntu/)
    > Note: Add the non-root user to the docker group by following [Manage Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).
2. [Install Visual Studio Code](https://code.visualstudio.com/download)
3. Install [Azure IoT Tools Extension](https://marketplace.visualstudio.com/items?itemName=vsciot-vscode.azure-iot-tools) for visual studio code.
## Setting up Cloud Resources
1. Create [Azure Resourse Group](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal#create-resource-groups)
2. Create [Azure IoT Hub](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-create-through-portal#create-an-iot-hub)
<a id="iotedge"> </a>
3. Create Azure IoT Edge Device using [Register your device](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-provision-single-device-linux-symmetric?view=iotedge-2020-11&tabs=azure-portal#register-your-device) section.
3. Create [Azure Video Analyzer Account](https://docs.microsoft.com/en-us/azure/azure-video-analyzer/video-analyzer-docs/edge/get-started-detect-motion-emit-events-portal#create-a-video-analyzer-account-in-the-azure-portal)
    > Note: While creating Azure Storage Account for Video Analyzer, select **standard general-purpose v2** as storage account type.
<a id="ava-edge"> </a>
4. Create an Azure Video Analyzer Edge Module by following the below steps
    
    1. Navigate to your Video Analyzer Account Created on the previous step.
    2. Navigate to **Edge > Edge Module**
    3. Select **Edge Module** from the top navigation bar and click on **Add Edge Module** to create an edge module.
    4. Copy the **Provisioning token** generated for the edge module and store it.
<a id="container-registry"> </a>
5. Create [Azure Container Registry](https://docs.microsoft.com/en-us/azure/azure-video-analyzer/video-analyzer-docs/edge/get-started-detect-motion-emit-events-portal#create-a-container-registry).
## Setting Up Deployment Machine
1. Copy the cloned repo to the deployment machine.

2. Follow the below steps to setup the edge deployment machine.

    ```sh
    cd <path to repo>/rs1-crowd-analytics/deployment/

    chmod +x setup.sh

    sudo setup.sh
    ```

    The setup script that ran on the above step will do the following
    * Installs Docker 
    * Installs Azure IoT Edge for Linux version 1.2
    * Prepares the IoT Edge Devices 
3. Copy the **Primary Connection String** of your Azure IoT Edge by navigating to **IoT Hub > `Your IoT Hub Name` > Device Management > IoT Edge > `Your IoT Edge Device ID`** on Azure Portal.
4. Run the below commands to connect your edge machine with Azure IoT Edge device

    ```sh
    sudo iotedge config mp --connection-string 'PASTE_DEVICE_CONNECTION_STRING_HERE'

    sudo iotedge config apply
    ```

# Deploying the Solution
> Note: This step assumes that you have successfully completed [Setting up Development Machine](setting-up-development-machine).

> These steps needs to be done from your development machine **not** deployment machine. If the development machine setup is not done, follow [Setting up Development machine](#setting-ip-development-machine).
## Connect Visual Studio Code to the IoT Hub
1. Follow [Obtain your IoT Hub connection string](https://docs.microsoft.com/en-us/azure/azure-video-analyzer/video-analyzer-docs/edge/get-started-detect-motion-emit-events-portal#obtain-your-iot-hub-connection-string) to copy your IoT Hub connection string.
2. Open the **Explorer** tab by naviagting to **View > Explorer** on the Visual Studio Code
2.  Open **Azure IOT HUB** from the lower-left corner of your visual studio code on **Explore Tab**.
3.  Click on the **More Action** to set the IoT Hub Connection string and paste the Primary Connection String copied on step 1 on the pop up input box shown and press **Enter** key.
4. After successfull setup, **Azure IOT HUB** from the lower-left corner of your visual studio code will list the IoT Edge Devices under your Azure IoT Hub.

## Building and Pushing Docker images
1. Open the cloned repo in the Visual Studio Code using **File > Open Folder**
2. Expand the **src** folder.
3. Update the **.env** file with the following details
    
    * `CONTAINER_REGISTRY_USERNAME` and `CONTAINER_REGISTRY_PASSWORD` from the container registry created on step [Create Azure Container Registry](#container-registry).
    
        * Navigate to **Settings > Access Keys** and enable Admin User.
        * use the **Registry name** and **password** to update the file.
    * `AVA_PROVISIONING_TOKEN` created on step [Create Azure Video Analyzer Edge Device](#ava-edge).

4. Right click on the `src/deployment.template.json` and then select **Build and Push IoT Edge Solution**.

## Deploying the Solution
Continue to deploy the solution to your deployment machine once all the module are build and pushed.

1. Right clik on the `src/config/deployment.amd64.json` file and select **Generate Deployment for Single Device**.
2. Selet the IoT Edge Device ID on the pop box that appears.
3. An OUTPUT window will pop up confirming that the deployment has succeeded.

## Verify the deployment
The deployment can be verified in multiple ways, here we will be verifying the deployment directly on deployment machine.

1. Open a terminal on your deployment machine.
2. Run the following command to list all the deployed modules

    ```sh
    sudo iotedge list
    ```
3. Wait until the following modules appear on the list with status as running
    * edgeAgent
    * edgeHub
    * grafana
    * crowd_telegraf
    * rtsp
    * avaextension
    * MQTTBroker
    * avaedge

    Run the command on step 2 to recheck the module status.

The same can be viewed from Visual Studio Code - Azure IOT HUB panel and Azure IoT Hub portal.

# Create and Deploy Crowd Analytics Pipeline
Follow the below steps to create and deploy Crowd Analytics Pipeline.
1. Open the IoT Edge created by navigating to **IoT Hub > Your IoT Hub Name > Device Management > IoT Edge > Your IoT Edge Device ID** on Azure Portal.
2. From the list of module shown, click on **avaedge** and select **Direct Method** from top-left.
3. Enter the following details and Click on **Invoke Method** to set the pipeline topology.
    
    * Method Name

        `pipelineTopologySet`
    * Payload

        Copy the content of the file `cloud_service_config/ava/topology.json`.

4. Check for the `201` status on the **Result** box for successfull completion of the method call.

5. Set the live pipeline for first camera stream using the following details to **Invoke Method**

    * Method Name

        `livePipelineSet`
    * Payload

        Copy the content of the file `cloud_service_cnfig/ava/live_pipeline_1.json`

6. Set the live pipeline for second camera stream using the following details to **Invoke Method**

    * Method Name

        `livePipelineSet`
    * Payload

        Copy the content of the file `cloud_service_cnfig/ava/live_pipeline_2.json`
7. Activate the pipeline created by invoking method using the below details

    1. First camera stream pipeline
        * Method Name
    
            `livePipelineActivate`
        * Payload

            ```json
            {
                "@apiVersion": "1.1",
                "name": "demostream1"
            }

    2. Second camera stream pipeline
        * Method Name
            
            `livePipelineActivate`
        * Payload
            ```json
            {
                "@apiVersion": "1.1",
                "name": "demostream2"
            }

# Visualize Crowd Analytics Edge UI
Follow the below steps to visualize the results using Crowd Analytics Edge UI.

1. On your deployment machine, open the [`localhost:3000`](http://localhost:3000) to open the Grafana UI.
    > If you are accessing the UI from a different machine, forward the ports `3000` and `5100` to the machine.
2. Use the following credentials to login
    * Username: `admin`
    * Password: `admin`
3. Click on the **Search** icon on the left navbar and select **Crowd Analytics Edge UI v1**.