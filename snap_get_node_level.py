#!/usr/bin/python3
import os
from svcoutglob import svc_out_glob

os.chdir('logs')
dirs = filter(os.path.isdir, os.listdir())
print('------')
for dir in dirs:
    files = os.listdir("%s/dumps"%dir)
    for file in files:
       if file.startswith('svcout.7'):
          svc_info_glob = svc_out_glob("%s/dumps/%s"%(dir,file))
          print(svc_info_glob['lsnode'][0]['site_id'])
          for lsnode in svc_info_glob['lsnode_delim']:
             print(lsnode['code_level'])
    print('------')
