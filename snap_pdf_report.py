#!/usr/bin/python3
import datetime
import os
import operator
from svcoutglob import svc_out_glob
from svcoutint import svc_out_int
from saout import sa_out
from pdfcreater import report_pdf

os.chdir('logs')
dirs = filter(os.path.isdir, os.listdir())
print('------')
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
          for lsdrive in svc_info_int['lsdrive']:
            drive_list.append({"id" : lsdrive['id'], "slotid" : lsdrive['slot_id'] , "status" : lsdrive['status']})
          sorted_drive_list = sorted(drive_list, key = lambda i: int(i['slotid']))

       if file.startswith('svcout.7'):
          svc_info_glob = svc_out_glob("%s/dumps/%s"%(dir,file))

    print('Create pdf for %s - %s - %s'%(saout_data['lsservicestatus'][0]['product_mtm'],saout_data['lsservicestatus'][0]['product_serial'],datetime.datetime.strptime(dir[-13:-7], "%y%m%d").date()))
    #format data block
    pdf_data_pac.update({'product_name':saout_data['lsservicestatus'][0]['product_name']})
    pdf_data_pac.update({'product_mtm':saout_data['lsservicestatus'][0]['product_mtm']})
    pdf_data_pac.update({'product_serial':saout_data['lsservicestatus'][0]['product_serial']})
    pdf_data_pac.update({'node_code_version':saout_data['lsservicestatus'][0]['node_code_version']})
    pdf_data_pac.update({'snap_date':datetime.datetime.strptime(dir[-13:-7], "%y%m%d").date()})
    pdf_data_pac.update({'drive_list':sorted_drive_list})
    pdf_data_pac.update({'node_list':svc_info_glob['lsnode_delim']})
    pdf_data_pac.update({'enclosure_list':svc_info_int['lsenclosure_delim']})
    pdf_data_pac.update({'mdisk_list':svc_info_glob['lsmdisk_delim']})
    pdf_data_pac.update({'mdiskgrp_list':svc_info_glob['lsmdiskgrp_delim']})
    pdf_data_pac.update({'vdisk_list':svc_info_glob['lsvdisk_delim']})
   # Create pdf file
    report_pdf("../reports/report%s.pdf"%dir,pdf_data_pac)