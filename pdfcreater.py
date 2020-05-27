from fpdf import FPDF, HTMLMixin

class MyFPDF(FPDF, HTMLMixin):
    pass

def li(title):
    html = ''
    html += "<li><font face='DejaVuSans'>%s :</font></li>"%(title)
    return (html)

def pdf_html_htable(keys,keys_width,values,values_width):
    html = ''
    html_track=[]
    html += "<table border=1>"
    header=True
    for key in keys:
        if header:
            html_track.append("<tr><th align='right' width=%s>%s</th>"%(keys_width,key))
        else:
            html_track.append("<tr><td align='right' width=%s>%s</td>"%(keys_width,key))
        header=False
    for line in values:
        i=0
        for value in line:
            if (i==0):
                html_track[i] += "<th width='%s' align='center'>%s</th>"%(values_width, value)
            else:
                html_track[i] += "<td width='%s' align='center'>%s</td>"%(values_width, value)
            i += 1
    for data in html_track:
        html += data+"</tr>"
    html += "</table>"
    return(html)

def pdf_html_vtable(keys,col_width,values):
    html = ''
    html += "<table border=1><tr>"
    i=0
    for key in keys:
        html += "<th align='center' width=%s>%s</th>"%(col_width[i],key)
        i += 1
    html += "</tr>"
    html += "<tbody>"
    for line in values:
        html += "<tr>"
        i=0
        for value in line:
            html += "<td width='%s' align='center'>%s</td>"%(col_width[i], value)
            i += 1
        html += "</tr>"
    html += "</tbody>"
    html += "</table>"
    return(html)

def report_pdf(filename,pdf_data_pac):
    pdf = MyFPDF()
    pdf.add_page()
    html = ''
    pdf.add_font('DejaVuSans', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVuSans', '', 18)
    pdf.cell(200,10, txt='Snap report', ln=1, align='C')

# System data
    html += '<table border=0>'
    html += '<tr><td width=340 align="right"><font face="DejaVuSans"> Model : </font></td><td width=360> %s</td></tr>'%(pdf_data_pac['product_name'])
    html += '<tr><td width=340 align="right"><font face="DejaVuSans"> Type : </font></td><td width=360> %s</td></tr>'%(pdf_data_pac['product_mtm'])
    html += '<tr><td width=340 align="right"><font face="DejaVuSans"> Serial number : </font></td><td width=360> %s</td></tr>'%(pdf_data_pac['product_serial'])
    html += '<tr><td width=340 align="right"><font face="DejaVuSans"> Firmware version : </font></td><td width=360> %s</td></tr>'%(pdf_data_pac['node_code_version'])
    html += '<tr><td width=340 align="right"><font face="DejaVuSans"> Snap collection date : </font></td><td width=360> %s</td></tr>'%(pdf_data_pac['snap_date'])
    html += '</table>'

    html += '<ul>'
# Enclosure list
    keys = ['serial_num','id','nodes','PSUs','status']
    col_width = [250,90,90,90,90]
    values=[]
    for enclosure in pdf_data_pac['enclosure_list']:
        values.append([enclosure['serial_number'],enclosure['id'],"%s/%s"%(enclosure['online_canisters'],enclosure['total_canisters']),"%s/%s"%(enclosure['online_PSUs'],enclosure['total_PSUs']),enclosure['status'][0:-4]])
    html += li('Enclosures')
    html += pdf_html_vtable(keys, col_width, values)

# Node list
    keys = ['panel_name','node_id','config','status']
    col_width = [250,90,90,90]
    values=[]
    for node in pdf_data_pac['node_list']:
        values.append([node['panel_name'],node['id'],node['config_node'],node['status'][0:-4]])
    html += li('Nodes')
    html += pdf_html_vtable(keys, col_width, values)

# Disks status table
    #pdf.cell(0,6, txt="Диски : ", ln=1, align="L")
    html += li('Drives')
    keys = ['slot_id','disk_id','status']
    for enclosure in pdf_data_pac['enclosure_list']:
        values=[]
        html += '%s / %s'%(enclosure['serial_number'],enclosure['id'])
        for drive in pdf_data_pac['drive_list']:
            if (drive['enclosure_id'] == enclosure['id']):
                values.append([drive['slot_id'],drive['id'],drive['status'][0:-4]])
        html += pdf_html_htable(keys, 90, values, 40)

# Mdiskgrp list
    keys = ['name','id','vdisks','status']
    col_width = [340,90,90,90]
    values=[]
    for mdiskgrp in pdf_data_pac['mdiskgrp_list']:
        values.append([mdiskgrp['name'],mdiskgrp['id'],mdiskgrp['vdisk_count'],mdiskgrp['status'][0:-4]])
    html += li('mdisk_grp')
    html += pdf_html_vtable(keys, col_width, values)

# Mdisk list
    keys = ['name','id','raid','status']
    col_width = [340,90,90,90]
    values=[]
    for mdisk in pdf_data_pac['mdisk_list']:
        values.append([mdisk['name'],mdisk['id'],mdisk['raid_level'],mdisk['status'][0:-4]])
    html += li('mdisk')
    html += pdf_html_vtable(keys, col_width, values)

    html += "</ul>"
    pdf.write_html(html)
    html='<ul>'
#    pdf.add_page()

# Vdisk list
    keys = ['name','id','md_grp','pf_node','status']
    col_width = [340,90,90,90,90]
    values=[]
    for vdisk in pdf_data_pac['vdisk_list']:
        if len(vdisk['name'])>19:
            name=vdisk['name'][0:8]+"..."+vdisk['name'][-8:]
        else:
            name=vdisk['name']
        values.append([name,vdisk['id'],vdisk['mdisk_grp_id'],vdisk['preferred_node_id'],vdisk['status'][0:-4]])
    html += li('vdisk')
    html += pdf_html_vtable(keys, col_width, values)
#
    html += "</ul>"

    pdf.write_html(html)
    pdf.output(filename+'.pdf')

def report_pdf_html(filename,name,type,serial_num,code_version,snap_date,disks):
    pdf = MyFPDF(format='letter')
    pdf.add_page()
    html = u"<center><H1>Testing page</H1></center><br>"
    html +=u"Модель : %s <br>"%name
    html +=u"Тип : %s<br>"%(type)
    pdf.add_font('DejaVuSans', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVuSans')
    pdf.write_html(html)
    pdf.output("%s.pdf"%filename, 'F')

if __name__ == "__main__":
    report_pdf('test',)