import requests
import json
from Services import *
import requests
import time
server_url = 'http://39.106.138.175/scene/download/'
headers = {'Content-Type': 'application/json'}

scene_dict = {}

#ReadServices = []
#ControlServices = []

class trigger():
    def __init__(self, readservice_aid, readservice_iid, condition, value):
        self.read_service = ReadService(readservice_aid, readservice_iid)
        self.condition = condition
        self.value = value
    
    def isTriggered(self):
        if(self.read_service.allowercondition==0):
            print("Condition: Equal - 0")
            print('Present HB value: ' + str(self.read_service.get_value()))
            print('Scene value: ' + str(self.value))
            return self.read_service.get_value() == self.value
        else :
            if(self.condition == 0):
                print("Condition: Smaller - 1")
                print('Present HB value: ' + str(self.read_service.get_value()))
                print('Scene value: ' + str(self.value))
                return  self.value > self.read_service.get_value()
            elif(self.condition == 1):
                print("Condition: Equal - 1")
                print('Present HB value: ' + str(self.read_service.get_value()))
                print('Scene value: ' + str(self.value))
                return self.read_service.get_value() == self.value
            elif(self.condition == 2):
                print("Condition: Bigger - 1")
                print('Present HB value: ' + str(self.read_service.get_value()))
                print('Scene value: ' + str(self.value))
                return self.value < self.read_service.get_value()
            else:
                print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "Scene.py: Error condition")

class action():
    def __init__(self, controlservice_aid, controlservice_iid, value):
        self.control_service = ControlService(controlservice_aid, controlservice_iid)
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
            tr = trigger(scenes[i]['trigger']['readserviceid']//10000, scenes[i]['trigger']['readserviceid']%10000, scenes[i]['trigger']['condition'], scenes[i]['trigger']['value'])
            ac = action(scenes[i]['action']['controlserviceid']//10000, scenes[i]['action']['controlserviceid']%10000, scenes[i]['action']['value'])
            if(tr.isTriggered()):
                ac.act()
                print("scenes[" + str(i) + '] is triggered')
                print('-------------------------------------------------------------------')
            else:
                print("scenes[" + str(i) + '] is not triggered')
                print('-------------------------------------------------------------------')
            del tr
            del ac
        time.sleep(10)
        try:
            response_server = requests.get(url=server_url)
            with open('/home/pi/Scripts/Scenes.json', 'w') as fo:
                fo.write(response_server.text)
        except:
            print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "Scene.py: SceneToServer Server no Response")

if __name__ == "__main__":
    SceneLoop()