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
with open('/home/pi/Scripts/Devices.json') as f:
    data_dict = json.load(f)
with open('/home/pi/Scripts/Services.json') as f:
    service_dict = json.load(f)
# In[]
sendAll = 1
while 1:
    current_dict = {'sensors':[], 'accessories':[]}
    for i in range(len(data_dict['sensors'])):
        try:
            url = ip + ':' + str(port) + '/characteristics?id=' + str(data_dict['sensors'][i]['aid']) + '.' + str(data_dict['sensors'][i]['iid'])
            r = requests.get(url)
            di = json.loads(r.text)
            data_dict['sensors'][i]['type']['currentvalue'] = di['characteristics'][0]['value']
            current_dict['sensors'].append(data_dict['sensors'][i])
            print('Current ' + data_dict['sensors'][i]['name'] + ' value:' + str(data_dict['sensors'][i]['type']['currentvalue']))
        except:
            print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "DataToServer.py: Local Django no Response")

    for i in range(len(data_dict['accessories'])):
        try:
            for j in range(len(data_dict['accessories'][i]['iids'])):
                url = ip + ':' + str(port) + '/characteristics?id=' + str(data_dict['accessories'][i]['aid']) + '.' + str(data_dict['accessories'][i]['iids'][j]['iid'])
                r = requests.get(url)
                di = json.loads(r.text)
                #print(di)
                if(data_dict['accessories'][i]['iids'][j]['currentvalue'] != di['characteristics'][0]['value']):
                    data_dict['accessories'][i]['iids'][j]['currentvalue'] = di['characteristics'][0]['value']
                    current_dict['accessories'].append(data_dict['accessories'][i])
                print('Current ' + data_dict['accessories'][i]['name'] + ' value:' + str(data_dict['accessories'][i]['iids'][j]['currentvalue']))
        except:
            print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "DataToServer.py: HB no Response")
    # Send to Server
    try:
        if(sendAll == 1):
            response_server = requests.post(url=server_device_url, headers=headers, data=json.dumps(data_dict))
            sendAll = 0
        else:
            response_server = requests.post(url=server_device_url, headers=headers, data=json.dumps(current_dict))
        current_dict = {'sensors':[], 'accessories':[]}
        # Status Refresh
        # Alarm Switch
        try:
            ServerResponse_dict = json.loads(response_server.text)
            #alarm = alarm_control_service()
            #lamp_1 = lamp_control_service_1()
            #lamp_2 = lamp_control_service_2()

            try:
                # Power switch of all accessories
                for i in range(len(data_dict['accessories'])):
                    for j in range(len(ServerResponse_dict['accessories'])):
                        try:
                            if(data_dict['accessories'][i]['aid'] == ServerResponse_dict['accessories'][j]['aid']):
                                #print(data_dict['accessories'][i]['iids'][0]['currentvalue'])
                                #print(ServerResponse_dict['accessories'][i]['iids'][0]['currentvalue'])
                                try:
                                    if(data_dict['accessories'][i]['iids'][0]['currentvalue'] != ServerResponse_dict['accessories'][j]['iids'][0]['currentvalue']):
                                        data_dict['accessories'][i]['iids'][0]['currentvalue'] = ServerResponse_dict['accessories'][j]['iids'][0]['currentvalue']
                                        Control = ControlService(data_dict['accessories'][i]['aid'], data_dict['accessories'][i]['iids'][0]['iid'])
                                        Control.set_value(data_dict['accessories'][i]['iids'][0]['currentvalue'])
                                except:
                                    print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "DataToServer.py: Control Service Error")
                        except:
                            print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "DataToServer.py: ServerResponse_dict Value['accessories'][j]['aid'] Error")
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
    time.sleep(5)