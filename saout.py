def key_checker(key,dict):
   orgkey = key
   i = 2
   while key in dict:
      key = orgkey
      key += '_%s'%i
      i += 1
   return key

def out_serv_recom_parser(file):
   file.seek(0)
   block = []
   for ln in file:
      if ln.startswith('sainfo lsservicerecommendation'):
         data = next(file)
         header = data.rstrip()
         recommendations = ''
         values = {}
         while data != '\n':
            data = next(file)
            recommendations+=data.rstrip()
         values.update({header:recommendations})
         block.append(values)
         return block

def out_blk_space_parser(file,cmd):
   file.seek(0)
   block = []
   for ln in file:
      if ln.startswith(cmd):
         data = next(file)
         header = data.rstrip().split()
         data = next(file)
         while data != '\n':
            split_data = data.rstrip().split()
            values = {}
            for i in range(0, len(header)):
               if i>len(split_data)-1:
                  values.update({header[i]: ''})
               else:
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
            split_data = data.rstrip().split()
            name=split_data[0]
            if len(split_data)>1:
               value=''
               for i in range(1,len(split_data)):
                  value += split_data[i]
                  if (len(split_data) > 1 and i < len(split_data)-1):
                     value += ' '
            else:
               value=''
            if name in values:
               name = key_checker(name,values)
               values.update({name: value})
            else:
               values.update({name:value})
            data=next(file)
         block.append(values)
   return block

def sa_out(infile):
   file = open(infile,'+r')
   sa_data={}
   sa_data.update({'lsservicestatus': out_line_parser(file, 'sainfo lsservicestatus')})
   sa_data.update({'lscmdstatus': out_line_parser(file, 'sainfo lscmdstatus')})
   sa_data.update({'lsservicenodes': out_blk_space_parser(file, 'sainfo lsservicenodes')})
   sa_data.update({'lsservicerecommendation': out_serv_recom_parser(file)})
   sa_data.update({'lshardware': out_line_parser(file, 'sainfo lshardware')})
   sa_data.update({'lscanister': out_line_parser(file, 'sainfo lscanister')})
   file.close()
   return sa_data