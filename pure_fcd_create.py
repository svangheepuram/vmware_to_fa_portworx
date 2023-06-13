#!/usr/bin/python3

from tools import cli, tasks, disk, pbmhelper
from pyVim import connect
from pyVmomi import vmodl, vim
from pure_read_json_contents import read_vmware_json

def create_fcd_disks(appname="dummy",size=1024):
  vmware_content=read_vmware_json()

  service_instance = connect.SmartConnectNoSSL(host=vmware_content['vmware']['vcenter'],\
          user=vmware_content['vmware']['user'],\
          pwd=vmware_content['vmware']['password'],\
          port=443)
  content=service_instance.RetrieveContent()
  datastore=disk.get_obj(content, [vim.Datastore], vmware_content['vmware']['vvolds'])
  spec = vim.vslm.CreateSpec()
  spec.name = appname
  print(size)
  spec.capacityInMB= round(size/(1024*1024))
  spec.backingSpec = vim.vslm.CreateSpec.DiskFileBackingSpec()
  spec.backingSpec.provisioningType = "thin"
  spec.backingSpec.datastore = datastore
  storage = content.vStorageObjectManager
  task = storage.CreateDisk_Task(spec)
  tasks.wait_for_tasks(service_instance, [task])

