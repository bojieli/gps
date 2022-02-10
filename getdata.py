#!/usr/bin/env python3
from urllib.request import http
import xml.etree.ElementTree as ET
import datetime
import os

conn = http.client.HTTPConnection('www.gps902.net', port=6601)

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
response = conn.getresponse()
response_data = response.read()
xmltree = ET.fromstring(response_data)

base_folder = os.path.join(os.path.dirname(__file__), 'data/')
date = datetime.datetime.now().strftime("%Y%m%d")
file_name = date + '.json'
file_path = os.path.join(base_folder, file_name)
f = open(base_folder + file_name, mode='w')
f.write(xmltree[0][0][0].text)
f.close()
