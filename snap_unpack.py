#!/usr/bin/python3

import os
import tarfile

#print (os.listdir('logs'))

os.chdir('/root/ya_snap_show/logs')

dir_content = os.listdir()

for file in dir_content:
    if (file[-4:] == '.tgz'):
       print(file[:-4])
       if not os.path.exists(file[:-4]):
          os.mkdir(file[:-4])
          tar = tarfile.open(file,'r:gz')
          tar.extractall(file[:-4])
          tar.close()
