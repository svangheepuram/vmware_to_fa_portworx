#!/usr/bin/python3
import os
import sys
import getopt
import argparse
import time
from kubernetes import client, config
from requirements import install_all_requirements
from vmotion import vmotion_from_vmfs_to_vvol
from pure_read_json_contents import *
from pure_get_data_disks import *
from pure_fcd_create import *
from purevolops import *


def input_args():
  parser = argparse.ArgumentParser(description="Migrate Application data from VM to Pure Storage and Portworx")
  parser.add_argument('--VMname', help="Input Virtual Machine Name",required=True)
  parser.add_argument('--Application', help="Input Application Name",required=True)
  parser.add_argument('--Kubeconfig', help="Input Kubeconfig file",required=True)
  args=parser.parse_args()
  return args

input=input_args()
sourcevm=input.VMname
appname=input.Application
kube_config=input.Kubeconfig

print("INFO Install all required packages and tools")
install_all_requirements()
print("INFO: VMware Vmotion from VMFS to VVOL")

vmotion_from_vmfs_to_vvol(sourcevm)
print("INFO: Get FlashArray data disks for VVOL")

data_disks=get_data_disks(sourcevm)
vmware_info=read_vmware_json()
count=1

for each_data_disk in data_disks:
    appname=appname + str(count)

    print("INFO: Create FCD disks with size" + str(each_data_disk['size']))
    create_fcd_disks(appname, size=each_data_disk['size'])

    print("INFO: Get Matching FCD disk from Pure Storage FA")
    fcd_disk_name=get_fcd_disks(each_data_disk['size']).split("/")
    vgroup_name=fcd_disk_name[0]
    vol_name=fcd_disk_name[1]

    print("INFO: Rename FCD with Application Name" + appname)
    pure_rename_vol(vgroup_name, vol_name, appname)

    target_appname=vgroup_name+"/"+appname
    print("INFO: Copy data from VVOL to FCD instantly using purevol copy")
    pure_overwrite_vol(each_data_disk['name'],target_appname)

    print("INFO: Generate Persistent Volume Claim yaml files")
    cmd="cp ./pvc.yaml" + " " + appname + "." + "yaml"
    os.system(cmd)

    print("INFO: Set pvcname for Portworx pvc")
    cmd="sed -i \'s/name:/name: " + "pvc" + appname + "/g' " + appname + "." + "yaml"
    os.system(cmd)

    print("INFO: Set Appname for Portworx PVC  ")
    cmd="sed -i \'s/app:/app: " + appname + "/g' " + appname + "." + "yaml"
    os.system(cmd)

    print("INFO: Set FlashArray Volume Size in PVC ")
    cmd="sed -i \'s/storage:/storage: " + str(each_data_disk['size']) + "/g' " + appname + "." + "yaml"
    os.system(cmd)

    print("INFO: Create px-pure-secret")
    cmd="kubectl create secret generic px-pure-secret --namespace kube-system --from-file=pure.json"
    os.system(cmd)

    print("INFO: Generate and Apply necessary Storage Class, PVC")
    cmd="kubectl apply -f px_sc.yaml"
    os.system(cmd)

    print("INFO: Create Portworx Persistent Volume Claim")
    cmd="kubectl apply -f" + " " + appname + "." + "yaml"
    os.system(cmd)

    time.sleep(30)
    print("INFO: Get Portworx PVC bound name")
    pvcappname="pvc"+appname 
    pvc=pv_name(kube_config, pvcappname)
    print(pvc)

    print("INFO: Get matching volume from array")
    portworx_data_disk=get_pvc_disks(pvc)

    print("INFO: Migrate data from FCD to Portworx")
    pure_overwrite_vol(target_appname,portworx_data_disk)

    print("The Portworx datadisk is "+ portworx_data_disk)









