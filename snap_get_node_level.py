#!/usr/bin/python3
import os
from svcoutglob import svc_out_glob
from svcoutint import svc_out_int
from saout import sa_out

os.chdir('logs')
dirs = filter(os.path.isdir, os.listdir())
print('------')
for dir in dirs:
    files = os.listdir("%s/dumps"%dir)
    for file in files:
       if file.startswith('saout.'):
           saout_data = sa_out("%s/dumps/%s"%(dir,file))
           print(saout_data['lsservicerecommendation'][0]['service_action'])
           print(saout_data['lshardware'])
       if file.startswith('svcout.int'):
          svc_info_int = svc_out_int("%s/dumps/%s"%(dir,file))
          #print (svc_info_int['lsdrive'])
          #print(svc_info_int['lsenclosure_delim'][0])
          #for lsdrive in svc_info_int['lsdrive']:
          #  print("id: %s - slotid: %s"%(lsdrive['id'],lsdrive['slot_id']))
       if file.startswith('svcout.7'):
          svc_info_glob = svc_out_glob("%s/dumps/%s"%(dir,file))
          print(svc_info_glob['lsnode'][0]['enclosure_serial_number'])
          for lsnode in svc_info_glob['lsnode_delim']:
             print(lsnode['code_level'])
    print('------')
