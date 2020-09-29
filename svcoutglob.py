def lsnode_parser(file):
   file.seek(0)
   for ln in file:
      if ln.startswith("svcinfo lsnode"):
         data=next(file)
         header = data.rstrip().split(':')
         data=next(file)
         block = []
         while data!='\n':
            split_data = data.rstrip().split(':')
            values = {}
            for i in range(0,len(header)):
               if i<10:
                 values.update({header[i]:split_data[i]})
               if i == 10:
                  values.update({header[i]:split_data[i]+":"+split_data[i+1]})
               else:
                 values.update({header[i]:split_data[i+1]})
            block.append(values)
            data=next(file)
         return block

def lsportip_parser(file):
   file.seek(0)
   for ln in file:
      if ln.startswith("svcinfo lsportip"):
         data=next(file)
         header = data.rstrip().split(':')
         data=next(file)
         block = []
         while data!='\n':
            split_data = data.rstrip().split(':')
            values = {}
            if split_data[10] == '':
               for i in range(0,len(header)):
                  values.update({header[i]:split_data[i]})
            else:
               for i in range(0,8):
                 values.update({header[i]:split_data[i]})
               values.update({header[9]:"%s:%s:%s:%s:%s:%s"%(split_data[9],split_data[10],split_data[11],split_data[12],split_data[13],split_data[14])})
               for i in range(10,len(header)):
                  values.update({header[i]:split_data[i+5]})
            block.append(values)
            data=next(file)
         return block

def out_space_events_parser(file,cmd):
   file.seek(0)
   for ln in file:
      if ln.startswith(cmd):
         data = next(file)
         header = data.rstrip().split()
         if (data[113:121]=="event_id"):
            print(data[113:121])
            marker_set = [[0,15],[16,30],[31,42],[46,55],[63,90],[91,98],[99,106],[107,112],[113,121],[122,132],[133,200]]
         elif (data[105:112]=="event_id"]):
            print(data[105:112])
            marker_set = [[0,15],[16,30],[31,42],[43,52],[53,64],[83,90],[91,98],[99,104],[105,113],[114,124],[125,190]]
         else:
            print("ELSE")
            marker_set = [[0,14],[16,27],[31,45],[47,62],[64,77],[78,84],[85,92],[93,98],[99,107],[108,118],[119,180]]
         data = next(file)
         block = []
         while data != '\n':
            values = {}
            for i in range(len(header)):
               values.update({header[i]: data[marker_set[i][0]:marker_set[i][1]].rstrip()})
            #print(values)
            block.append(values)
            data = next(file)
         return block

def out_dot_parser(file,cmd):
   file.seek(0)
   for ln in file:
      if ln.startswith(cmd):
         data=next(file)
         header = data.rstrip().split(':')
         data=next(file)
         block = []
         while data!='\n':
            split_data = data.rstrip().split(':')
            values = {}
            for i in range(0,len(header)):
               values.update({header[i]:split_data[i]})
            block.append(values)
            data=next(file)
         return block

def out_line_parser(file,cmd):
   file.seek(0)
   block = []
   for ln in file:
      if ln.startswith(cmd):
         data = next(file)
         values = {}
         while data!='\n':
            split_data = data.rstrip().split(':')
            name=split_data[0]
            value=split_data[1]
            values.update({name:value})
            data=next(file)
         block.append(values)
   return block

def svc_out_glob(infile):
   file = open(infile,'+r')
   svc_info_glob={}
   print(bool(svc_info_glob))
   svc_info_glob.update({'lsnode':lsnode_parser(file)})
   svc_info_glob.update({'lsnode_delim':out_line_parser(file,'svcinfo lsnode -delim : ')})
   svc_info_glob.update({'lsvdisk': out_dot_parser(file, 'svcinfo lsvdisk')})
   svc_info_glob.update({'lshost': out_dot_parser(file, 'svcinfo lshost')})
   svc_info_glob.update({'lshost_delim': out_line_parser(file, 'svcinfo lshost -delim : ')})
   svc_info_glob.update({'lshostcluster': out_dot_parser(file, 'svcinfo lshostcluster')})
   svc_info_glob.update({'lshostclustervolumemap': out_dot_parser(file, 'svcinfo lshostclustervolumemap')})
   svc_info_glob.update({'lshostvdiskmap': out_dot_parser(file, 'svcinfo lshostvdiskmap')})
   svc_info_glob.update({'lsportsas': out_dot_parser(file, 'svcinfo lsportsas')})
   svc_info_glob.update({'lsquorum': out_dot_parser(file, 'svcinfo lsquorum')})
   svc_info_glob.update({'lsmdiskgrp': out_dot_parser(file, 'svcinfo lsmdiskgrp')})
   svc_info_glob.update({'lseventlog': out_dot_parser(file, 'svcinfo lseventlog  -delim :')})
   if not svc_info_glob['lseventlog']:
     svc_info_glob.update({'lseventlog': out_space_events_parser(file, 'svcinfo lseventlog -alert')})
     #print("lseventlog: %s"%svc_info_glob['lseventlog'])
   svc_info_glob.update({'lssystem': out_line_parser(file, 'svcinfo lssystem')})
   svc_info_glob.update({'lsupdate': out_line_parser(file, 'svcinfo lsupdate')})
   svc_info_glob.update({'lsencryption': out_line_parser(file, 'svcinfo lsencryption')})
   svc_info_glob.update({'lsportusb': out_dot_parser(file, 'svcinfo lsportusb')})
   svc_info_glob.update({'lssecurity': out_line_parser(file, 'svcinfo lssecurity')})
   svc_info_glob.update({'lsfeature': out_dot_parser(file, 'svcinfo lsfeature')})
   svc_info_glob.update({'lslicense': out_line_parser(file, 'svcinfo lslicense')})
   svc_info_glob.update({'lssra': out_line_parser(file, 'svcinfo lssra')})
   svc_info_glob.update({'lskeyserverisklm': out_line_parser(file, 'svcinfo lskeyserverisklm')})
   svc_info_glob.update({'lskeyserverkeysecure': out_line_parser(file, 'svcinfo lskeyserverkeysecure')})
   svc_info_glob.update({'lstargetportfc': out_dot_parser(file, 'svcinfo lstargetportfc')})
   svc_info_glob.update({'lscloudcallhome': out_line_parser(file, 'svcinfo lscloudcallhome')})
   svc_info_glob.update({'lshostiplogin': out_dot_parser(file, 'svcinfo lshostiplogin')})
   svc_info_glob.update({'lshostiplogin_delim': out_dot_parser(file, 'svcinfo lshostiplogin -delim : ')})
   svc_info_glob.update({'lssystemethernet': out_line_parser(file, 'svcinfo lssystemethernet')})
   svc_info_glob.update({'lsldap': out_line_parser(file, 'svcinfo lsldap')})
   svc_info_glob.update({'lsuser': out_dot_parser(file, 'svcinfo lsuser')})
   svc_info_glob.update({'lsuser_delim': out_line_parser(file, 'svcinfo lsuser -delim : ')})
   svc_info_glob.update({'lsusergrp': out_dot_parser(file, 'svcinfo lsusergrp')})
   svc_info_glob.update({'lsusergrp_delim': out_line_parser(file, 'svcinfo lsusergrp -delim : ')})
   svc_info_glob.update({'lsmdisk': out_dot_parser(file, 'svcinfo lsmdisk')})
   svc_info_glob.update({'lsmdiskgrp': out_dot_parser(file, 'svcinfo lsmdiskgrp')})
   svc_info_glob.update({'lsmdisk_delim': out_line_parser(file, 'svcinfo lsmdisk -delim : ')})
   svc_info_glob.update({'lsmdiskgrp_delim': out_line_parser(file, 'svcinfo lsmdiskgrp -delim : -gui ')})
   svc_info_glob.update({'lsvdisk': out_dot_parser(file, 'svcinfo lsvdisk')})
   svc_info_glob.update({'lsvdisk_delim': out_line_parser(file, 'svcinfo lsvdisk -delim : ')})
   svc_info_glob.update({'lsportip': lsportip_parser(file)})
   svc_info_glob.update({'lsportfc': out_dot_parser(file, 'svcinfo lsportfc')})
   svc_info_glob.update({'lsportfc_delim': out_line_parser(file, 'svcinfo lsportfc -delim : ')})
   svc_info_glob.update({'lspartnership': out_dot_parser(file, 'svcinfo lspartnership')})
   svc_info_glob.update({'lspartnership_delim': out_line_parser(file, 'svcinfo lspartnership -delim : ')})
   svc_info_glob.update({'lsemailuser': out_dot_parser(file, 'svcinfo lsemailuser')})
   svc_info_glob.update({'lsemailuser_delim': out_line_parser(file, 'svcinfo lsemailuser -delim : ')})
   file.close()
   return svc_info_glob
