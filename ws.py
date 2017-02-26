import websocket
import json
import os
import sys
import datetime

os.chdir(os.path.dirname(os.path.realpath(__file__)))

ws = websocket.WebSocket()
ws.connect("wss://node.imibaby.net:8443/svc/pipe")

SID = None
with open('SID.key') as f:
    SID = f.read()

# hello
SN = 1
need_login = True
if SID:
    ws.send(json.dumps({"CID":20091,"Version":"00000000","SN":SN,"SID":SID}))
    SN += 1
    x = json.loads(ws.recv())
    if x['RC'] == 1:
        need_login = False

# login
if need_login:
    ws.close()
    ws.connect("wss://node.imibaby.net:8443/svc/pipe")
    ws.send('{"CID":10011,"Version":"00000000","SN":1707552991,"SID":"495ADBA64AF841AC8F49D797605C3AE1","PL":{"Type":102,"Password":"DF8143C12B13FBEA958D3F5224E0A21F","Name":"xiaomi@2.0:rqWHdgHaDltkdScJsZs3\/jVbEKA="}}')
    new_login = json.loads(ws.recv())
    try:
        SID = new_login['SID']
        with open('SID.key', 'w') as f:
            f.write(SID)
        #print('Login SID: ' + SID)
    except:
        print('Login failed:')
        print(new_login)
        ws.close()

today = datetime.date.today().strftime('%Y%m%d')

# user basic info
#ws.send(json.dumps({"CID":20091,"Version":"00000000","SN":1709338253,"SID":SID}))
# check position
ws.send(json.dumps({"CID":50031,"Version":"00000000","SN":1708339662,"SID":SID,"PL":{"Size":1,"EID":"8F28166A5064D2763C4FA4AF7F0A41EF","Key":"78999898989898998"}}))
data = ws.recv()
with open('data/live-position.json', 'w') as f:
    f.write(data)

# check status
ws.send(json.dumps({"CID":60051,"Version":"00000000","SN":1700645968,"SID":SID,"PL":{"EID":"8F28166A5064D2763C4FA4AF7F0A41EF","Keys":["battery_level","watch_status","operation_mode_value","signal_level","device_power_on_time","SleepList","SilenceList","status"]}}))
data = ws.recv()
with open('data/status.json', 'w') as f:
    f.write(data)

# 6 days at most
# ws.send('{"CID":50051,"Version":"00000000","SN":1701252870,"SID":"D5098C549D5340C9BFA459820265FB64","PL":{"EID":"8F28166A5064D2763C4FA4AF7F0A41EF","Date":["20170131","20170130","20170129","20170128","20170127","20170126"]}}')
# 5 days
ws.send(json.dumps({"CID":50051,"Version":"00000000","SN":1701252870,"SID":SID,"PL":{"EID":"8F28166A5064D2763C4FA4AF7F0A41EF","Date":[today]}}))
# check one day
#ws.send(json.dumps({"CID":50051,"Version":"00000000","SN":1699552280,"SID":SID,"PL":{"EID":EID,"Date":["20170131"]}}))
data = ws.recv()
with open('data/' + today + '.json', 'w') as f:
    f.write(data)

ws.close()
