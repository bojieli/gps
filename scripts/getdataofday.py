#!/usr/bin/env python3
from urllib.request import http
import xml.etree.ElementTree as ET
import datetime
import os
import json
import sys

conn = http.client.HTTPConnection('www.gps902.net', port=6601)

# load today's history
headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://tempuri.org/GetDevicesHistory",
        "User-Agent": "TTWL/1.0 CFNetwork/1312 Darwin/21.0.0"
}

def hour_min_to_str(hour):
    return str(hour) if hour >= 10 else '0' + str(hour)

datetimes = dict()
if len(sys.argv) >= 2:
    date = sys.argv[1]
    date = date[0:4] + '/' + date[4:6] + '/' + date[6:8]
else:
    date = datetime.datetime.now().strftime("%Y/%m/%d")
for hour in range(0, 24):
    for minute in range(0, 6):
        minute = minute * 10
        begin_time = hour_min_to_str(hour) + ':' + hour_min_to_str(minute)
        if minute == 50:
            if hour == 23:
                end_time = '23:59'
            else:
                end_time = hour_min_to_str(hour + 1) + ':' + hour_min_to_str(0)
        else:
            end_time = hour_min_to_str(hour) + ':' + hour_min_to_str(minute + 10)

        request_body = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body>
<GetDevicesHistory xmlns="http://tempuri.org/"><DeviceID>2357349</DeviceID><StartTime>''' + date + ''' ''' + begin_time + '''</StartTime><EndTime>''' + date + ''' ''' + end_time + '''</EndTime><TimeZones>China Standard Time</TimeZones><MapType>Google</MapType><ShowLBS>0</ShowLBS><SelectCount>10000</SelectCount><Key>7DU2DJFDR8321</Key></GetDevicesHistory></soap:Body>
</soap:Envelope>'''

        conn.request('POST', '/TutuAPI.asmx', body=request_body, headers=headers)
        response = conn.getresponse().read()
        xmltree = ET.fromstring(response)
        today_history = xmltree[0][0][0].text

        try:
            history_points = json.loads(today_history)['devices']
            for point in history_points:
                if point["pt"] not in datetimes:
                    point["positionTime"] = point["pt"]
                    point.pop("pt")
                    datetimes[point["positionTime"]] = point
        except:
            pass

base_folder = os.path.join(os.path.dirname(__file__), '..', 'data/')
if len(sys.argv) >= 2:
    date = sys.argv[1]
else:
    date = datetime.datetime.now().strftime('%Y%m%d')
file_name = 'status-' + date + '.json'
file_path = os.path.join(base_folder, file_name)
dedup_data = [datetimes[key] for key in sorted(datetimes)]
with open(file_path, mode='w') as f:
    f.write(json.dumps(dedup_data))
