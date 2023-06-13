import subprocess
import os
from pure_read_json_contents import read_vmware_json


def vmotion_from_vmfs_to_vvol(source="source"):


    vmware_content=read_vmware_json()
    os.environ['GOVC_URL']=vmware_content['vmware']['vcenter']
    os.environ['GOVC_INSECURE']=str(1)
    os.environ['GOVC_USERNAME']=vmware_content['vmware']['user']
    os.environ['GOVC_PASSWORD']=vmware_content['vmware']['password']
    os.environ['GOVC_DATASTORE']=vmware_content['vmware']['vvolds']
    os.environ['GOVC_DATACENTER']=vmware_content['vmware']['dc']
    os.environ['GOVC_CLUSTER']=vmware_content['vmware']['cluster']
#    os.environ['GOVC_RESOURCE_POOL']=vmware_content['vmware']['cluster']+'/'+'Resources'
    command="govc vm.migrate -ds " + vmware_content['vmware']['vvolds'] + " " + source
    os.system(command)

