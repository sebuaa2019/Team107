# In[]
import requests
import json
import time
import random
from Services import *

key = '031-45-155'
ip = 'http://localhost'
server_url = 'http://39.106.138.175/device/upload/'
port = 39000
headers = {'Content-Type': 'application/json'}

# In[]
with open('/home/pi/Scripts/DataTemplate.json') as f:
    load_dict = json.load(f)
# In[]
while 1:
    for i in range(len(load_dict['sensors'])):
        url = ip + ':8000/sensor_db/'
        try:
            r = requests.get(url)
            di = json.loads(r.text)
            load_dict['sensors'][i]['type']['currentvalue'] = di[load_dict['sensors'][i]['key']]
        except:
            print("DataToServer.py: Local Django no Response")

    for i in range(len(load_dict['accessories'])):
        try:
            for j in range(len(load_dict['accessories'][i]['iids'])):
                url = ip + ':' + str(port) + '/characteristics?id=' + str(load_dict['accessories'][i]['aid']) + '.' + str(load_dict['accessories'][i]['iids'][j]['iid'])
                r = requests.get(url)
                di = json.loads(r.text)
                load_dict['accessories'][i]['iids'][j]['currentvalue'] = di['characteristics'][0]['value']
        except:
            print("DataToServer.py: HB no Response")
    # Send to Server
    try:
        response_server = requests.post(url=server_url, headers=headers, data=json.dumps(load_dict))
        # Status Refresh
        # Alarm Switch
        ServerResponse_dict = json.loads(response_server.text)
        alarm = alarm_control_service()
        if(ServerResponse_dict['sensors'][2]['type']['currentvalue']):     
            alarm.set_value(True)
        else:
            alarm.set_value(False)
    except:
        print("DataToServer.py: Server no Response")
    time.sleep(10)