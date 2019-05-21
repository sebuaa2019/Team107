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
sendAll = 1
while 1:
    current_dict = {'sensors':[], 'accessories':[]}
    for i in range(len(data_dict['sensors'])):
        url = ip + ':8000/sensor_db/'
        try:
            r = requests.get(url)
            di = json.loads(r.text)
            data_dict['sensors'][i]['type']['currentvalue'] = di[data_dict['sensors'][i]['key']]
            current_dict['sensors'].append(data_dict['sensors'][i])
        except:
            print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "DataToServer.py: Local Django no Response")

    for i in range(len(data_dict['accessories'])):
        try:
            for j in range(len(data_dict['accessories'][i]['iids'])):
                url = ip + ':' + str(port) + '/characteristics?id=' + str(data_dict['accessories'][i]['aid']) + '.' + str(data_dict['accessories'][i]['iids'][j]['iid'])
                r = requests.get(url)
                di = json.loads(r.text)
                if(data_dict['accessories'][i]['iids'][j]['currentvalue'] != di['characteristics'][0]['value']):
                    data_dict['accessories'][i]['iids'][j]['currentvalue'] = di['characteristics'][0]['value']
                    current_dict['accessories'].append(data_dict['accessories'][i])
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
            alarm = alarm_control_service() #aid=7
            lamp_1 = lamp_control_service_1()   #aid=8
            lamp_2 = lamp_control_service_2()   #aid=9

            try:
                #if(ServerResponse_dict['accessories'][2]['iids'][0]['currentvalue']==True and data_dict['accessories'][2]['iids'][0]['currentvalue']==False):     
                #    alarm.set_value(True)
                #elif(ServerResponse_dict['accessories'][2]['iids'][0]['currentvalue']==False and data_dict['accessories'][2]['iids'][0]['currentvalue']==True):
                #    alarm.set_value(False)

                # Power switch of all accessories
                for i in range(len(data_dict['accessories'])):
                    for j in range(len(ServerResponse_dict['accessories'])):
                        if(data_dict['accessories'][i]['aid'] == ServerResponse_dict['accessories'][j]['aid']):
                            if(data_dict['accessories'][i]['iids'][0]['currentvalue'] != ServerResponse_dict['accessories'][i]['iids'][0]['currentvalue']):
                                data_dict['accessories'][i]['iids'][0]['currentvalue'] = ServerResponse_dict['accessories'][i]['iids'][0]['currentvalue']
                                if(data_dict['accessories'][i]['aid']==7):
                                    alarm.set_value(data_dict['accessories'][i]['iids'][0]['currentvalue'])
                                elif(data_dict['accessories'][i]['aid']==8):
                                    lamp_1.set_value(data_dict['accessories'][i]['iids'][0]['currentvalue'])
                                elif(data_dict['accessories'][i]['aid']==9):
                                    lamp_2.set_value(data_dict['accessories'][i]['iids'][0]['currentvalue'])
                                else:
                                    print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "DataToServer.py:  Invalid aid")

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