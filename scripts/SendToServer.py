import requests
import json

key = '123-45-678'
ip = 'http://localhost'
port = 39000


with open('./DataTemplate.json') as f:
    load_dict = json.load(f)

while 1:
    for i in range(len(load_dict['sensors'])):
        load_dict['sensors'][i]['type']['currentvalue'] = db
    for i in range(len(load_dict['accessories'])):
        for j in range(len(load_dict['accessories'][i]['iids'])):
            url = ip + ':' + str(port) + '/characteristics?id=' + str(load_dict['accessories'][i]['aid']) + '.' + str(load_dict['accessories'][i]['iids'][j]['iid'])
            r = requests.get(url)
            di = json.loads(r.text)
            load_dict['accessories'][i]['iids'][j]['currentvalue'] = di['characteristics'][0]['value']