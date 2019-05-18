# In[]
import requests
import json
import time
import random

key = '031-45-155'
ip = 'http://192.168.50.69'
#server_url = 'http://39.106.138.175/device/upload/'
headers = {'Content-Type': 'application/json'}

# In[]
with open('./Scenes.json') as f:
    load_dict = json.load(f)
# In[]
while 1:
    # Send to Server
    try:
        response_server = requests.post(purl=server_url, headers=headers, data=json.dumps(load_dict))
        with open('./Scenes.json') as fo:
            fo.write(json.dumps(response_server.text,ensure_ascii=False,indent=2))
    time.sleep(30)
