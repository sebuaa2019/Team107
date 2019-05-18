# In[]
import requests
import json
import time
import random
server_url = 'http://39.106.138.175/scene/uploadScene/'
headers = {'Content-Type': 'application/json'}

# In[]
with open('/home/pi/Scripts/Scenes.json') as f:
    load_dict = json.load(f)
# In[]
while 1:
    # Send to Server
    try:
        response_server = requests.post(purl=server_url, headers=headers, data=json.dumps(load_dict))
        with open('./Scenes.json') as fo:
            fo.write(json.dumps(response_server.text,ensure_ascii=False,indent=2))
    except:
        print("SceneToServer.py: Server no Response")
    time.sleep(30)
