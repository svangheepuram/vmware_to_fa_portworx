# How to Start?

./pure_vm_to_px.py

usage: pure_vm_to_px.py [-h]  
       --VMname <vmname>   
       --Application <application name>   
       --Kubeconfig  < path to kubeconfig file>   

for ex: pure_vm_to_px.y --VMname Oracle_2.6 --Application Oracle --Kubeconfig /home/oracle/kubeconfig  

## Pre-requisites:

Edit vmware.json and fill Vcenter details of VM location  
Edit pure.json and fill FlashArray details   



## What next?  

1. Mount the PVC with mountPath: in your App.   
2. The container should should be able to access the data, with read and write access.

