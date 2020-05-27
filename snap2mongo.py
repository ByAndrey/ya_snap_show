import datetime
import os
import operator
from svcoutglob import svc_out_glob
from svcoutint import svc_out_int
from saout import sa_out
from pymongo import MongoClient

os.chdir('logs')
dirs = filter(os.path.isdir, os.listdir())
print('------')
global_snap_collector = {}
client = MongoClient()
db = client.test
post = db.test
for dir in dirs:
    files = os.listdir("%s/dumps"%dir)
    pdf_data_pac = {}
    for file in files:

       if file.startswith('saout.'):
           saout_data = sa_out("%s/dumps/%s"%(dir,file))

       if file.startswith('svcout.int'):
          svc_info_int = svc_out_int("%s/dumps/%s"%(dir,file))

       if file.startswith('svcout.7'):
          svc_info_glob = svc_out_glob("%s/dumps/%s"%(dir,file))

    print('Getting data from %s - %s - %s'%(saout_data['lsservicestatus'][0]['product_mtm'],saout_data['lsservicestatus'][0]['product_serial'],datetime.datetime.strptime(dir[-13:], "%y%m%d.%H%M%S")))
    post_id = post.insert_one({"mtm":saout_data['lsservicestatus'][0]['product_mtm'],"sn":saout_data['lsservicestatus'][0]['product_serial'],"timestamp":dir[-13:],"saout":saout_data,"svcout_int":svc_info_int,"svcout_glob":svc_info_glob}).inserted_id
    print(post_id)
    # Create pdf file
    global_snap_collector.update({'%s %s'%(saout_data['lsservicestatus'][0]['product_serial'],datetime.datetime.strptime(dir[-13:], "%y%m%d.%H%M%S")) : {"saout":saout_data,"svcout_int":svc_info_int,"svcout_glob":svc_info_glob}})