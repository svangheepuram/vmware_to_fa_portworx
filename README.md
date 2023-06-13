How to start?
./pure_vm_to_px.py
usage: pure_vm_to_px.py [-h] --VMname VMNAME --Application APPLICATION
                        --Kubeconfig KUBECONFIG
pure_vm_to_px.py: error: the following arguments are required: --VMname, --Application, --Kubeconfig

What is needed?
Edit vmware.json and fill Vcenter details of VM location
Edit pure.json and fill FlashArray details 


What next?
The data is copied to Portworx Persistent Volume. All you have to mount it in K8s with "mountPath: /data". 
Application running in K8s can use Portworx Volume to serve the data.
