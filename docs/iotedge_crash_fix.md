# Workaround to fix modules failing to start after restart

The document is to fix `permission denied on workload socket` which shows up after a edge device restart.

*Note: This document is based on the issue [edgeAgent doesn't start after reboot - permission denied ](https://github.com/Azure/iotedge/issues/5672) created for the same on [Azure iotedge](https://github.com/Azure/iotedge) github repo.*

*Note: This fix is applicable only for the Azure iotedge version 1.2.**

If any one or all of the below modules failing to start after a edge device reboot or iotedge restart.

* `avaedge`
* `edgeAgent`
* `edgeHub`

Follow the below steps;

1. Delete the folder `/var/lib/aziot/edged/mnt/`

    ```s
    sudo rm -rf /var/lib/aziot/edged/mnt/
    ```

2. Restart iotedge

    ```sh
    sudo iotedge system restart
    ```

*Note: If you are using Azure iotedge version `1.1.*`, the release with fix to the above mentioned issue is release `1.1.8`.*
