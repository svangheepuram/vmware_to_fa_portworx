from kubernetes import client, config
import purestorage as ps
from pure_read_json_contents import read_pure_json

# Never do this in prod. SSL warnings are there for a reason. but for a demo, they are the worst.
import urllib3
urllib3.disable_warnings()

def pure_vol_snap(vol_name):
    pure_info=read_pure_json()
    array = ps.FlashArray(pure_info['FlashArrays'][0]['MgmtEndPoint'], api_token=pure_info['FlashArrays'][0]['APIToken'])
    make_snap = array.create_snapshot(vol_name)
    temp_name = make_snap
    temp_name = str(temp_name)
    list_name = temp_name.split(",")
    list_name = list_name[3].strip("'name': ")
    make_snap = list_name
    return make_snap

def list_snap(vol_name):
    pure_info=read_pure_json()
    array = ps.FlashArray(pure_info['FlashArrays'][0]['MgmtEndPoint'], api_token=pure_info['FlashArrays'][0]['APIToken'])
    get_snap = array.get_volume(vol_name, snap=True)
    return get_snap

def pure_overwrite_vol(source_volume, destination_volume):
    pure_info=read_pure_json()
    array = ps.FlashArray(pure_info['FlashArrays'][0]['MgmtEndPoint'], api_token=pure_info['FlashArrays'][0]['APIToken'])
    new_vol = array.copy_volume(source_volume, destination_volume, overwrite=True)
    return new_vol

def pure_rename_vol(vgroup_name, source_volume, destination_volume):
    pure_info=read_pure_json()
    array = ps.FlashArray(pure_info['FlashArrays'][0]['MgmtEndPoint'], api_token=pure_info['FlashArrays'][0]['APIToken'])
    source=vgroup_name+"/"+source_volume
    destination=vgroup_name+"/"+destination_volume
    print(source)
    print(destination)
    new_vol = array.rename_volume(source,destination)
    return new_vol

def pure_vol_info():
    pure_info=read_pure_json()
    array = ps.FlashArray(pure_info['FlashArrays'][0]['MgmtEndPoint'], api_token=pure_info['FlashArrays'][0]['APIToken'])
    get_info = array.list_volumes(tags=True)
    get_info_str = str(get_info)
    temp_str = get_info_str.replace('"', "")
    temp_list = temp_str.split('}')
    match_list = [s for s in temp_list if vol_name in s]
    temp_name = match_list
    temp_name = str(temp_name)
    list_name = temp_name.split(",")
    list_name = get_info_str
    return list_name
