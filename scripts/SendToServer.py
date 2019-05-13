# In[]
import requests
import json
import time
import random

key = '031-45-155'
ip = 'http://192.168.50.69'
server_url = ''
port = 39000
headers = {'Content-Type': 'application/json'}

# In[]
with open('./DataTemplate.json') as f:
    load_dict = json.load(f)
# In[]
while 1:

    for i in range(len(load_dict['sensors'])):
        #url = ip + ':' + str(port) + '/characteristics?id=' + str(load_dict['sensors'][i]['aid']) + '.' + str(load_dict['sensors'][i]['iid'])
        #r = requests.get(url)
        #di = json.loads(r.text)
        #load_dict['accessories'][i]['type']['currentvalue'] = di['characteristics'][0]['value']
        url = ip + ':8000/sensor_db/'
        r = requests.get(url)
        di = json.loads(r.text)
        load_dict['sensors'][i]['type']['currentvalue'] = di[load_dict['sensors'][i]['key']]


    for i in range(len(load_dict['accessories'])):
        for j in range(len(load_dict['accessories'][i]['iids'])):
            url = ip + ':' + str(port) + '/characteristics?id=' + str(load_dict['accessories'][i]['aid']) + '.' + str(load_dict['accessories'][i]['iids'][j]['iid'])
            r = requests.get(url)
            di = json.loads(r.text)
            load_dict['accessories'][i]['iids'][j]['currentvalue'] = di['characteristics'][0]['value']
    
    # Send to Server
    #response_server = requests.post(url=server_url, headers=headers, data=json.dumps(load_dict))

    # Primary Notification
    occupancy_text = "主人SAMA, 你家可能被偷了( ´_ゝ｀)" + str(random.random())
    smoke_text = "主人SAMA, 你家可能着火了( ´_ゝ｀)" + str(random.random())
    server_chan_url = "https://sc.ftqq.com/SCU37298T847874b7bf139ffb4081081f070bcbbc5c0bc8a6a0078.send?"
    if(load_dict['accessories'][2]['iids'][0]['currentvalue']):
        print("Alarm On")
        if(load_dict['sensors'][2]['type']['currentvalue'] and load_dict['sensors'][3]['type']['currentvalue']):
            server_chan_url += "text=" + occupancy_text
            response_serverchan = requests.post(server_chan_url)
            sleep(15)
            server_chan_url += "text=" + smoke_text
            response_serverchan = requests.post(server_chan_url)
            print('Occupancy and Fire Alarm Triggered')
        elif(load_dict['sensors'][2]['type']['currentvalue']):
            server_chan_url += "text=" + occupancy_text
            response_serverchan = requests.post(server_chan_url)
            print('Occupancy Alarm Triggered')
        elif(load_dict['sensors'][3]['type']['currentvalue']):
            server_chan_url += "text=" + smoke_text
            response_serverchan = requests.post(server_chan_url)
            print('Fire Alarm Triggered')
    else:
        print("Alarm Off")
    time.sleep(3)