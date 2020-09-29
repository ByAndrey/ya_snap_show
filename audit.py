def out_line_parser(file,cmd):
   file.seek(0)
   block = []
   for ln in file:
      if ln.startswith(cmd):
         data = next(file)
         values = {}
         while data!='\n':
            split_data = data.rstrip().split(':')
            name=split_data[0].strip()
            value=split_data[1].strip()
            values.update({name:value})
            data=next(file)
         block.append(values)
   return block

def audit(infile):
    file = open(infile,'+r')
    audit_log = {}
    audit_log = out_line_parser(file, 'Auditlog Entry')
    file.close()
    return audit_log
