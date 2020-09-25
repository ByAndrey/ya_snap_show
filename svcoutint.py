def out_space_parser(file,cmd):
   file.seek(0)
   for ln in file:
      if ln.startswith(cmd):
         data = next(file)
         header = data.rstrip().split()
         data = next(file)
         block = []
         while data != '\n':
            split_data = data.rstrip().split()
            values = {}
            for i in range(0, len(header)):
               values.update({header[i]: split_data[i]})
            block.append(values)
            data = next(file)
         return block

def out_dot_parser(file,cmd):
   file.seek(0)
   for ln in file:
      if ln.startswith(cmd):
         data=next(file)
         if data != '\n':
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
         else:
            print("empty")

def out_dot_parser_multln(file,cmd):
   file.seek(0)
   block = []
   for ln in file:
      if ln.startswith(cmd):
         data = next(file)
         if data!='\n':
            header = data.rstrip().split(':')
            data = next(file)
         while data != '\n':
            split_data = data.rstrip().split(':')
            values = {}
            for i in range(0, len(header)):
               values.update({header[i]: split_data[i]})
            block.append(values)
            data = next(file)
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

def svc_out_int(infile):
   file = open(infile,'+r')
   svc_info_int={}
   svc_info_int.update({'lssasfabric': out_space_parser(file, 'svcinfo lssasfabric')})
   svc_info_int.update({'lsdrive':out_dot_parser(file,'svcinfo lsdrive')})
   svc_info_int.update({'lsdrive_delim': out_line_parser(file, 'svcinfo lsdrive -delim : ')})
   svc_info_int.update({'lsdriveprogress': out_line_parser(file, 'svcinfo lsdriveprogress -delim : ')})
   svc_info_int.update({'lsenclosure': out_dot_parser(file, 'svcinfo lsenclosure')})
   svc_info_int.update({'lsenclosure_delim': out_line_parser(file, 'svcinfo lsenclosure -delim : ')})
   svc_info_int.update({'lsenclosurebattery': out_dot_parser(file, 'svcinfo lsenclosurebattery')})
   svc_info_int.update({'lsenclosurebattery_delim': out_line_parser(file, 'svcinfo lsenclosurebattery -delim : ')})
   svc_info_int.update({'lsenclosurepsu': out_dot_parser(file, 'svcinfo lsenclosurepsu')})
   svc_info_int.update({'lsenclosurepsu_delim': out_line_parser(file, 'svcinfo lsenclosurepsu -delim : ')})
   svc_info_int.update({'lsenclosurecanister': out_dot_parser(file, 'svcinfo lsenclosurecanister')})
   svc_info_int.update({'lsenclosurecanister_delim': out_line_parser(file, 'svcinfo lsenclosurecanister -delim : ')})
   svc_info_int.update({'lsenclosureslot': out_dot_parser(file, 'svcinfo lsenclosureslot')})
   svc_info_int.update({'lsenclosureslot_delim': out_line_parser(file, 'svcinfo lsenclosureslot -delim : ')})
   svc_info_int.update({'lsenclosurecanister': out_dot_parser(file, 'svcinfo lsenclosurecanister')})
   svc_info_int.update({'lsarray': out_dot_parser(file, 'svcinfo lsarray')})
   svc_info_int.update({'lsarray_delim': out_line_parser(file, 'svcinfo lsarray -delim : ')})
   svc_info_int.update({'lsarraymember': out_dot_parser_multln(file, 'svcinfo lsarraymember ')})
   svc_info_int.update({'lsarraymembergoals': out_dot_parser_multln(file, 'svcinfo lsarraymembergoals ')})
   svc_info_int.update({'lsarrayinitprogress': out_dot_parser_multln(file, 'svcinfo lsarrayinitprogress ')})
   svc_info_int.update({'lsarraysyncprogress': out_dot_parser_multln(file, 'svcinfo lsarraysyncprogress ')})
   svc_info_int.update({'lsarraymemberprogress': out_dot_parser_multln(file, 'svcinfo lsarraymemberprogress ')})
   file.close()
   return svc_info_int