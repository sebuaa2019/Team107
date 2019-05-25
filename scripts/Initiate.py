import os
import json
import requests

with open('/home/pi/.homebridge/config.json',encoding = 'utf-8') as f:
    CONFIG = json.load(f)

Devices = {'sensors' : [], 'accessories' : []}
Scenes = {'scenes':[]}
Service_list = {
    "readservices": [
        {
            "aid": 0,
            "iid": 0,
            "name": "时间服务",
            "allowed_condition": 0
        }
    ],
    "controlservices": [
    ]
}

devices = []
accessory_names = []

for i in range(1, len(CONFIG['platforms'])):
    for j in range(len(CONFIG['platforms'][i]['deviceCfgs'])):
        accessory_names.append(CONFIG['platforms'][i]['deviceCfgs'][j]['Name'])
for i in range(len(CONFIG['accessories'])):
    accessory_names.append(CONFIG['accessories'][i]['name'])

ch = os.popen('/home/pi/searchCharac.sh > charac.txt').read()

with open('/home/pi/charac.txt') as f:
    for i in range(len(accessory_names)):
        grep_flg = 'grep -m 1 ' + accessory_names[i]
        command = 'cat charac.txt | ' + grep_flg
        devices.append(json.loads(os.popen(command).read()))

for i in range(len(devices)):
    for j in range(len(accessory_names)):
        if(devices[i]['characteristics'][0]['value'] == accessory_names[j]):
            HB_url = 'http://localhost:39000/characteristics?id=' + str(devices[i]['characteristics'][0]['aid']) + '.10'
            req = json.loads(requests.get(HB_url).text)
            if(isinstance(req['characteristics'][0]['value'], bool)):   #accessory
                acc_instance = {
                    'aid' : req['characteristics'][0]['aid'],
                    'name' : accessory_names[j], 
                    'iids':[
                        {
                            'iid':10, 
                            'valuetype' : 1, 
                            'currentvalue' : req['characteristics'][0]['value']
                        }
                    ]
                }
                Devices['accessories'].append(acc_instance)
            elif(isinstance(req['characteristics'][0]['value'], int)):  #sensor
                valuetype = 0 if(req['characteristics'][0]['value']>1) else 1
                sen_instance = {
                    'aid' : req['characteristics'][0]['aid'],
                    'iid' : 10,
                    'name' : accessory_names[j], 
                    'type':{
                        'valuetype' : valuetype,
                        'currentvalue' : req['characteristics'][0]['value']
                    }
                }
                Devices['sensors'].append(sen_instance)

with open('/home/pi/Scripts/Devices.json', 'w', encoding='utf-8') as f:
    json.dump(Devices, f)
#with open('/home/pi/Scripts/Scenes.json', 'w', encoding='utf-8') as f:
    #json.dump(Scenes, f)

for i in range(len(Devices['sensors'])):
    #allowed_condition = 1 if(req['characteristics'][0]['value']>1) else 0
    allowed_condition = 1 if(Devices['sensors'][i]['type']['valuetype']==0) else 0
    read_service_instance = {
        'aid' : Devices['sensors'][i]['aid'],
        'iid' : Devices['sensors'][i]['iid'],
        'name' : Devices['sensors'][i]['name'],
        'allowed_condition' : allowed_condition
    }
    Service_list['readservices'].append(read_service_instance)

for i in range(len(Devices['accessories'])):
    read_service_instance = {
        'aid' : Devices['accessories'][i]['aid'],
        'iid' : Devices['accessories'][i]['iids'][0]['iid'],
        'name' : Devices['accessories'][i]['name'] + '开关',
        'allowed_condition' : 0
    }
    Service_list['readservices'].append(read_service_instance)

for i in range(len(Devices['accessories'])):
    control_service_instance = {
        'aid' : Devices['accessories'][i]['aid'],
        'iid' : Devices['accessories'][i]['iids'][0]['iid'],
        'allowed_value' : 0,
        'name' : Devices['accessories'][i]['name'] + '开关',
    }
    Service_list['controlservices'].append(control_service_instance)

with open('/home/pi/Scripts/Services.json', 'w', encoding='utf-8') as f:
    json.dump(Service_list, f)