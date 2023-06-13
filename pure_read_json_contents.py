import json


def read_vmware_json():
  f=open("vmware.json","r")
  vmware_info=json.load(f)
  f.close()
  return(vmware_info)

def read_pure_json():
  f=open("pure.json","r")
  pure_info=json.load(f)
  f.close()
  return(pure_info)
