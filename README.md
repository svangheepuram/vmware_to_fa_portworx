# How to Start?

./pure_vm_to_px.py

usage: pure_vm_to_px.py [-h]  
       --VMname VMNAME   
       --Application APPLICATION  
       --Kubeconfig KUBECONFIG  


## Pre-requisites:

Edit vmware.json and fill Vcenter details of VM location  
Edit pure.json and fill FlashArray details   



## What next?  

1. Mount the PVC with mountPath: in your App.   
2. Application Container should read and write the data.  

