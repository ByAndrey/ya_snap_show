import xml.etree.ElementTree as ET
tree = ET.parse('logs/snap.7820TZB-1.200327.170223/dumps/iostats/Nv_stats_7820TZB-2_200327_165800')
root = tree.getroot()
#print (root.tag)
#print (root.attrib)
for child in root:
    print (child.attrib)
