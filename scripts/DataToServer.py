# In[]
import requests
import json
import time
import random
from Services import *

key = '031-45-155'
ip = 'http://localhost'
server_device_url = 'http://39.106.138.175/device/upload/'
server_service_url = 'http://39.106.138.175/scene/service/'

port = 39000
headers = {'Content-Type': 'application/json'}

# In[]
with open('/home/pi/Scripts/DataTemplate.json') as f:
    data_dict = json.load(f)
with open('/home/pi/Scripts/Service_List.json') as f:
    service_dict = json.load(f)
# In[]
while 1:
    for i in range(len(data_dict['sensors'])):
        url = ip + ':8000/sensor_db/'
        try:
            r = requests.get(url)
            di = json.loads(r.text)
            data_dict['sensors'][i]['type']['currentvalue'] = di[data_dict['sensors'][i]['key']]
        except:
            print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "DataToServer.py: Local Django no Response")

    for i in range(len(data_dict['accessories'])):
        try:
            for j in range(len(data_dict['accessories'][i]['iids'])):
                url = ip + ':' + str(port) + '/characteristics?id=' + str(data_dict['accessories'][i]['aid']) + '.' + str(data_dict['accessories'][i]['iids'][j]['iid'])
                r = requests.get(url)
                di = json.loads(r.text)
                data_dict['accessories'][i]['iids'][j]['currentvalue'] = di['characteristics'][0]['value']
        except:
            print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "DataToServer.py: HB no Response")
    # Send to Server
    try:
        response_server = requests.post(url=server_device_url, headers=headers, data=json.dumps(data_dict))
        # Status Refresh
        # Alarm Switch
        try:
            ServerResponse_dict = json.loads(response_server.text)
            alarm = alarm_control_service()
            try:
                if(ServerResponse_dict['accessories'][2]['iids'][0]['currentvalue']):     
                    alarm.set_value(True)
                else:
                    alarm.set_value(False)
            except:
                print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "DataToServer.py: ServerResponse_dict Value Error")
        except:
            print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "DataToServer.py: ServerResponse_dict loads failed")
    except:
        print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "DataToServer.py: Data post failed, Server no Response")

    try:
        requests.post(url=server_service_url, headers=headers, data=json.dumps(service_dict))
    except:
        print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "DataToServer.py: Service post failed, Server no Response")
    time.sleep(10)