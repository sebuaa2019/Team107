import os
import json

with open('/home/pi/.homebridge/config.json',encoding = 'utf-8') as f:
    CONFIG = json.load(f)

accessory_names = []

for i in range(len(CONFIG['platforms'][1]['deviceCfgs'])):
    accessory_names.append(CONFIG['platforms'][1]['deviceCfgs'][i]['Name'])
for i in range(len(CONFIG['accessories'])):
    accessory_names.append(CONFIG['accessories'][i]['name'])

