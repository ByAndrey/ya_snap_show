#!/usr/bin/python3
import datetime
import os
import operator
from svcoutglob import svc_out_glob
from svcoutint import svc_out_int
from saout import sa_out

os.chdir('sber_logs')
dirs = filter(os.path.isdir, os.listdir())
print('------')
global_snap_collector = {}
for dir in dirs:
    files = os.listdir("%s/dumps"%dir)
    pdf_data_pac = {}
    for file in files:

       if file.startswith('saout.'):
           saout_data = sa_out("%s/dumps/%s"%(dir,file))

       if file.startswith('svcout.int'):
          svc_info_int = svc_out_int("%s/dumps/%s"%(dir,file))
          drive_list = []
          #Sorted drive_list (sort by slot_id)
          #for lsdrive in svc_info_int['lsdrive']:
          #  drive_list.append({"id" : lsdrive['id'], "slotid" : lsdrive['slot_id'], "status" : lsdrive['status']})
          sorted_drive_list = sorted(svc_info_int['lsdrive'], key = lambda i: int(i['slot_id']))

       if file.startswith('svcout.7'):
          svc_info_glob = svc_out_glob("%s/dumps/%s"%(dir,file))

    print('Reading snap %s - %s - %s'%(saout_data['lsservicestatus'][0]['product_mtm'],saout_data['lsservicestatus'][0]['product_serial'],datetime.datetime.strptime(dir[-13:-7], "%y%m%d").date()))
    #print(svc_info_glob['lsvdisk'])
    print("Mdisk :")
    for mdisk in svc_info_glob['lsmdisk']:
        print(mdisk['name'])
    
    print("array member:")
    for member in svc_info_int['lsarraymember']:
      print(member)
    #print("Vdisk :")
    #for vdisk in svc_info_glob['lsvdisk']:
    #    print(vdisk['name'])
    #print("Hosts :")
    #for host in svc_info_glob['lshost']:
    #    print(host['name'])
    #print("lsdrive :")
    #for drive in svc_info_int['lsdrive_delim']:
    #    print("%s-%s [%s]"%(drive['enclosure_id'],drive['slot_id'],drive['mdisk_name']))
    #print('lsportip :')
    #for portip in svc_info_glob['lsportip']:
    #    if portip['IP_address'] != '':
    #        print("%s - %s - %s"%(portip['node_name'],portip['vlan'],portip['IP_address']))
    #        #print(portip)
print('--------')
