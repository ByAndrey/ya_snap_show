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
   svc_info_glob.update({'lsnode':out_dot_parser(file,'svcinfo lsnode')})
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
   svc_info_glob.update({'lseventlog': out_dot_parser(file, 'svcinfo lseventlog')})
   svc_info_glob.update({'lssystem': out_line_parser(file, 'svcinfo lssystem -delim : -gui')})
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
   svc_info_glob.update({'lsportfc': out_dot_parser(file, 'svcinfo lsportfc')})
   svc_info_glob.update({'lsportfc_delim': out_line_parser(file, 'svcinfo lsportfc -delim : ')})
   svc_info_glob.update({'lspartnership': out_dot_parser(file, 'svcinfo lspartnership')})
   svc_info_glob.update({'lspartnership_delim': out_line_parser(file, 'svcinfo lspartnership -delim : ')})
   svc_info_glob.update({'lsemailuser': out_dot_parser(file, 'svcinfo lsemailuser')})
   svc_info_glob.update({'lsemailuser_delim': out_line_parser(file, 'svcinfo lsemailuser -delim : ')})
   file.close()
   return svc_info_glob
