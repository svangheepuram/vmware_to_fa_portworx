import purestorage as ps
from pure_read_json_contents import read_pure_json
from kubernetes import client, config

# Never do this in prod. SSL warnings are there for a reason. but for a demo, they are the worst.
import urllib3
urllib3.disable_warnings()

def get_data_disks(vm):

    pure_info=read_pure_json()
    array = ps.FlashArray(pure_info['FlashArrays'][0]['MgmtEndPoint'], api_token=pure_info['FlashArrays'][0]['APIToken'])
    vol_list = array.list_volumes()
    vvol_list = [ vvols for vvols in vol_list if vm in vvols['name']]
    data_disk_list = [ data_disks for data_disks in vvol_list if 'Data' in data_disks['name']]
    sorted_list=sorted(data_disk_list,key=lambda d: d['created'])
    return sorted_list[1:]

def get_fcd_disks(size):
    pure_info=read_pure_json()
    array = ps.FlashArray(pure_info['FlashArrays'][0]['MgmtEndPoint'], api_token=pure_info['FlashArrays'][0]['APIToken'])
    vol_list = array.list_volumes()
    vvol_list = [ vvols for vvols in vol_list if 'fcd' in vvols['name']]
    data_disk_list = [ data_disks for data_disks in vvol_list if 'Data' in data_disks['name']]
    fcd_data_disk= [ each for each in data_disk_list if each['size'] == size ]
    return (fcd_data_disk[0]['name'])

def get_pvc_disks(pvc):
    pure_info=read_pure_json()
    array = ps.FlashArray(pure_info['FlashArrays'][0]['MgmtEndPoint'], api_token=pure_info['FlashArrays'][0]['APIToken'])
    vol_list = array.list_volumes()
    px_name=""
    for each in vol_list:
      if pvc in each['name']:
        px_name=each['name']
    return px_name

def pv_name(kube_config, pvc_name):
  config.load_kube_config(config_file=kube_config)
  v1 = client.CoreV1Api()
  px_name=""
  pvc_array = v1.list_persistent_volume_claim_for_all_namespaces(watch=False)
  for i in pvc_array.items:
    px_name=i.spec.volume_name
  return px_name


