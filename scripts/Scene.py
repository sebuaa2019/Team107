import requests
import json
from Services import *
import requests
import time
server_url = 'http://39.106.138.175/scene/download/'
headers = {'Content-Type': 'application/json'}

scene_dict = {}

ReadServices = []
ControlServices = []

def setup():
    ReadServices.append(time_service())
    ReadServices.append(temperature_service())
    ReadServices.append(humidity_service())
    ReadServices.append(smoke_service())
    ReadServices.append(occupancy_service())
    ReadServices.append(lamp_service_1())
    ReadServices.append(lamp_service_2())
    ReadServices.append(alarm_read_service())
    ControlServices.append(alarm_control_service())
    ControlServices.append(lamp_control_service_1())
    ControlServices.append(lamp_control_service_2())

class trigger():
    def __init__(self, readserviceid, condition, value):
        self.read_service = ReadServices[readserviceid]
        self.condition = condition
        self.value = value
    
    def isTriggered(self):
        if(self.read_service.allowercondition==0):
            return self.read_service.get_value() == self.value
        else :
            if(self.condition == 0):
                return self.read_service.get_value() < self.value
            elif(self.condition == 1):
                return self.read_service.get_value() == self.value
            elif(self.condition == 2):
                return self.read_service.get_value() > self.value
            else:
                print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "Scene.py: Error condition")

class action():
    def __init__(self, controlserviceid, value):
        self.control_service = ControlServices[controlserviceid]
        self.value = value
    
    def act(self):
        return self.control_service.set_value(self.value)


def SceneLoop():
    while(1):
        time.sleep(10)
        with open('/home/pi/Scripts/Scenes.json', 'r') as f:
            scene_dict = json.load(f)
            scenes = scene_dict['scenes']
        for i in range(len(scenes)):
            tr = trigger(scenes[i]['trigger']['readserviceid'], scenes[i]['trigger']['condition'], scenes[i]['trigger']['value'])
            ac = action(scenes[i]['action']['controlserviceid'], scenes[i]['action']['value'])
            if(tr.isTriggered()):
                ac.act()
            del tr
            del ac
        time.sleep(10)
        try:
            #response_server = requests.post(purl=server_url, headers=headers, data=json.dumps(scene_dict))
            response_server = requests.get(url=server_url)
            with open('/home/pi/Scripts/Scenes.json', 'w') as fo:
                fo.write(response_server.text)
        except:
            print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "Scene.py: SceneToServer Server no Response")

if __name__ == '__main__':
    setup()
    SceneLoop()