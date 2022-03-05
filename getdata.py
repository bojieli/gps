#!/usr/bin/env python3
from urllib.request import http
import xml.etree.ElementTree as ET
import datetime
import os
import json

conn = http.client.HTTPConnection('www.gps902.net', port=6601)

# load today's history
headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://tempuri.org/GetDevicesHistory",
        "User-Agent": "TTWL/1.0 CFNetwork/1312 Darwin/21.0.0"
}
date = datetime.datetime.now().strftime("%Y/%m/%d")
request_body = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body>
<GetDevicesHistory xmlns="http://tempuri.org/"><DeviceID>2357349</DeviceID><StartTime>''' + date + ''' 00:00</StartTime><EndTime>''' + date + ''' 23:59</EndTime><TimeZones>China Standard Time</TimeZones><MapType>Google</MapType><ShowLBS>0</ShowLBS><SelectCount>10000</SelectCount><Key>7DU2DJFDR8321</Key></GetDevicesHistory></soap:Body>
</soap:Envelope>'''

conn.request('POST', '/TutuAPI.asmx', body=request_body, headers=headers)
response = conn.getresponse().read()
xmltree = ET.fromstring(response)

# create the today history file
base_folder = os.path.join(os.path.dirname(__file__), 'data/')
date = datetime.datetime.now().strftime("%Y%m%d")
file_name = date + '.json'
file_path = os.path.join(base_folder, file_name)
f = open(file_path, mode='w')
today_history = xmltree[0][0][0].text
f.write(today_history)
f.close()

# load read-time status
headers["SOAPAction"] = "http://tempuri.org/GetTracking"
request_body = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body>
<GetTracking xmlns="http://tempuri.org/"><DeviceID>2357349</DeviceID><Model>0</Model><TimeZones>China Standard Time</TimeZones><MapType>Google</MapType><Language>zh-Hans-CN</Language><Key>7DU2DJFDR8321</Key></GetTracking></soap:Body>
</soap:Envelope>'''
conn.request('POST', '/TutuAPI.asmx', body=request_body, headers=headers)
response = conn.getresponse().read()

# create the real-time status file
xmltree = ET.fromstring(response)
file_name = 'status.json'
file_path = os.path.join(base_folder, file_name)
f = open(file_path, mode='w')
curr_status = xmltree[0][0][0].text
f.write(curr_status)
f.close()

# create the final today history file
file_name = 'status-' + date + '.json'
file_path = os.path.join(base_folder, file_name)
datetimes = dict()
try:
    with open(file_path, mode='r') as f:
        data = f.read()
        jsondata = json.loads(data)
        for point in jsondata:
            if point["positionTime"] not in datetimes:
                datetimes[point["positionTime"]] = point
except:
    pass

new_point = json.loads(curr_status)
if new_point["positionTime"] not in datetimes:
    datetimes[new_point["positionTime"]] = new_point

try:
    history_points = json.loads(today_history)['devices']
    for point in history_points:
        if point["pt"] not in datetimes:
            point["positionTime"] = point["pt"]
            point.pop("pt")
            datetimes[point["positionTime"]] = point
except:
    pass

dedup_data = [datetimes[key] for key in sorted(datetimes)]
with open(file_path, mode='w') as f:
    f.write(json.dumps(dedup_data))
