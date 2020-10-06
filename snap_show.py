#!/usr/bin/python3

from flask import Flask, request, render_template
from pymongo import MongoClient
from bson import ObjectId
import operator
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.environ['SNAP_DIR']

client = MongoClient()
db = client.test

def drive_info(system_id,drive_id):
   data = get_unit_data(system_id)
   drive_info = {}
   for drive in data['svcout_int']['lsdrive_delim']:
      if drive['id']==drive_id:
         drive_info.update({'drive_id' : drive_id })
         drive_info.update({'enc_id' : drive['enclosure_id']})
         drive_info.update({'mdisk_id' : drive['mdisk_id']})
         drive_info.update({'slot_id' : drive['slot_id']})
         drive_info.update({'drive_status' : drive['status']})
         if 'use' in drive:
            drive_info.update({'drive_use' : drive['use']})
         if 'transport_protocol' in drive:
            drive_info.update({'drive_type' : drive['transport_protocol']})
         if 'physical_capacity' in drive:
            drive_info.update({'drive_capacity' : drive['physical_capacity']})
         elif 'capacity' in drive:
            drive_info.update({'drive_capacity' : drive['capacity']}) 
         drive_info.update({'drive_fru' : drive['FRU_part_number']})
         if 'FRU_identity' in drive: 
            drive_info.update({'drive_identity': drive['FRU_identity']})
         drive_info.update({'drive_prodid' : drive['product_id']})
         drive_info.update({'drive_vendorid' : drive['vendor_id']})

   for enclosure in data['svcout_int']['lsenclosure_delim']:
      if enclosure['id'] == drive_info['enc_id']:
         drive_info.update({'enc_mtm' : enclosure['product_MTM']})
         drive_info.update({'enc_sn' : enclosure['serial_number']})
         drive_info.update({'enc_type' : enclosure['type']})

   for mdisk in data['svcout_int']['lsarray_delim']:
      if mdisk['mdisk_id']== drive_info['mdisk_id']:
         drive_info.update({'mdisk_name' : mdisk['mdisk_name']})
         drive_info.update({'mdisk_status' : mdisk['status']})
         drive_info.update({'mdisk_drivecount' : mdisk['drive_count']})
         drive_info.update({'mdisk_stripewidth' : mdisk['stripe_width']})
         drive_info.update({'mdisk_distributed' : mdisk['distributed']})
         drive_info.update({'mdisk_raidtype' : mdisk['raid_level']})
         drive_info.update({'mdisk_groupid' : mdisk['mdisk_grp_id']})
   return(drive_info)

def systems_list(mtm,sn):
   data = []
   if mtm and sn:
      x = db.test.find({'mtm':{'$regex':mtm},'sn':{'$regex':sn}}).sort('timestamp',-1).limit(20)
   elif mtm and not sn:
      x = db.test.find({'mtm':{'$regex':mtm}}).sort('timestamp',-1).limit(20)
   elif not mtm and sn:
      x = db.test.find({'sn':{'$regex':sn}}).sort('timestamp',-1).limit(20)
   else:
      x = db.test.find().sort('timestamp',-1).limit(20)
   for item in x:
      print("%s - %s - %s"%(item['mtm'],item['sn'],item['timestamp']))
      data.append([item['_id'],item['mtm'],item['sn'],item['timestamp'],item['saout']['lsservicestatus'][0]['node_code_version']])
   return(data)

def get_unit_data(id):
   item = db.test.find({"_id":ObjectId(id)})
   return (item[0])


@app.route("/", methods=['GET','POST'])
def home_page():
   if request.args.get('mtm'):
      mtm = request.args.get('mtm')
   else: mtm = ''
   if request.args.get('sn'):
      sn = request.args.get('sn')
   else: sn = ''
   data = systems_list(mtm,sn)
   return render_template("snap_show_main.html", mtm=mtm, sn=sn,data = data)

@app.route("/main", methods=['GET','POST'])
def main_page():
   if request.args.get('mtm'):
      mtm = request.args.get('mtm')
   else: mtm = ''
   if request.args.get('sn'):
      sn = request.args.get('sn')
   else: sn = ''
   data = systems_list(mtm,sn)
   return render_template("snap_show_main.html", mtm=mtm, sn=sn, data = data)

@app.route("/unit", methods=['GET','POST'])
def unit_page():
   if request.args.get('id') :
      sorted_drive_list = sorted(get_unit_data(request.args.get('id'))['svcout_int']['lsdrive_delim'], key = lambda i: i['slot_id'])
      if (request.args.get('type')=='config'):
         return render_template("unit_config.html", data = get_unit_data(request.args.get('id')))
      elif (request.args.get('type')=='firmware'):
         return render_template("unit_firmware.html", data = get_unit_data(request.args.get('id')))
      elif (request.args.get('type')=='events'):
         return render_template("unit_events.html", data = get_unit_data(request.args.get('id')))
      elif (request.args.get('type')=='audit'):
         return render_template("unit_audit.html", data = get_unit_data(request.args.get('id')))
      else:
         return render_template("unit_hardware.html", data = get_unit_data(request.args.get('id')), sorted_drive_list = sorted_drive_list)
   else:
      return render_template("snap_show_main.html",data = data)

@app.route("/upload", methods=['GET','POST'])
def upload_page():
   if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return render_template("snap_uploaded.html", filename = file.filename)
   else:
      return render_template("snap_show_upload.html")

@app.route("/drive_info", methods=['GET','POST'])
def drive_rep_page():
   if (request.args.get('id') and request.args.get('drive_id')) :
      drive = drive_info(request.args.get('id'),request.args.get('drive_id'))
      return render_template("drive_report.html", drive = drive)
   else:
      return main_page()

if __name__ == "__main__":
   app.run(host="0.0.0.0")
