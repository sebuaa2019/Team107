import time
import requests
import json

with open('./DataTemplate.json') as f:
    scene_dict = json.load(f)

class ReadService():
    def __init__(self):
        self.id = 0
        self.aid = 0
        self.iid = 0
        self.allowercondition = 0
    
    def get_value(self):
        return 0

class ControlService():
    def __init__(self):
        self.id = 0
        self.aid = 0
        self.iid = 0
        self.key = '031-45-155'
        self.allowedvalue = 0
    
    def set_value(self):
        return 0

class time_service(ReadService):
    def __init__(self):
        self.id = 0
        self.aid = 0
        self.iid = 0
        self.allowercondition = 0

    def get_value(self):
        localtime = time.localtime(time.time())
        return localtime.tm_hour+(localtime.tm_min/100)

class temperature_service(ReadService):
    def __init__(self):
        self.id = 1
        self.aid = 5
        self.iid = 10
        self.allowercondition = 1

    def get_value(self):
        r = requests.get('localhost:8000/sensor_db/')
        di = json.loads(r.text)
        return di["temperature"]

class humidity_service(ReadService):
    def __init__(self):
        self.id = 2
        self.aid = 5
        self.iid = 13
        self.allowercondition = 1

    def get_value(self):
        r = requests.get('localhost:8000/sensor_db/')
        di = json.loads(r.text)
        return di["humidity"]

class smoke_service(ReadService):
    def __init__(self):
        self.id = 3
        self.aid = 5
        self.iid = 19
        self.allowercondition = 0

    def get_value(self):
        r = requests.get('localhost:8000/sensor_db/')
        di = json.loads(r.text)
        return di["smoke"]

class occupancy_service(ReadService):
    def __init__(self):
        self.id = 4
        self.aid = 5
        self.iid = 25
        self.allowercondition = 0

    def get_value(self):
        r = requests.get('localhost:8000/sensor_db/')
        di = json.loads(r.text)
        return di["occupancy"]

class lamp_service_1(ReadService):
    def __init__(self):
        self.id = 5
        self.aid = 5
        self.iid = 25
        self.allowercondition = 0

    def get_value(self):
        url = 'localhost:39000/characteristics?id=' + str(self.aid) + '.' + str(self.iid)
        r = requests.get(url)
        di = json.loads(r.text)
        return di["value"]

class lamp_service_2(ReadService):
    def __init__(self):
        self.id = 6
        self.aid = 5
        self.iid = 25
        self.allowercondition = 0

    def get_value(self):
        url = 'localhost:39000/characteristics?id=' + str(self.aid) + '.' + str(self.iid)
        r = requests.get(url)
        di = json.loads(r.text)
        return di["value"]

class alarm_read_service(ReadService):
    def __init__(self):
        self.id = 7
        self.aid = 5
        self.iid = 25
        self.allowercondition = 0

    def get_value(self):
        url = 'localhost:39000/characteristics?id=' + str(self.aid) + '.' + str(self.iid)
        r = requests.get(url)
        di = json.loads(r.text)
        return di["value"]

class alarm_control_service(ControlService):
    def __init__(self):
        self.id = 0
        self.aid = 7
        self.iid = 10
    
    def set_value(self, value):
        Raspberry_headers = {'authorization': self.key}
        Raspberry_url = 'http://localhost:39000/characteristics' 
        data = '{"characteristics":[{"aid":' + str(self.aid) + ',"iid":' + str(self.iid) + ',"value":' + str(value).lower() + ',"status":0}]}'
        r = requests.put(url=Raspberry_url,headers=Raspberry_headers,data=data)

class lamp_control_service_1(ControlService):
    def __init__(self):
        self.id = 1
        self.aid = 2
        self.iid = 10
    
    def set_value(self, value):
        Raspberry_headers = {'authorization': self.key}
        Raspberry_url = 'http://localhost:39000/characteristics' 
        data = '{"characteristics":[{"aid":' + str(self.aid) + ',"iid":' + str(self.iid) + ',"value":' + str(value).lower() + ',"status":0}]}'
        r = requests.put(url=Raspberry_url,headers=Raspberry_headers,data=data)

class lamp_control_service_2(ControlService):
    def __init__(self):
        self.id = 2
        self.aid = 3
        self.iid = 10
    
    def set_value(self, value):
        Raspberry_headers = {'authorization': self.key}
        Raspberry_url = 'http://localhost:39000/characteristics' 
        data = '{"characteristics":[{"aid":' + str(self.aid) + ',"iid":' + str(self.iid) + ',"value":' + str(value).lower() + ',"status":0}]}'
        r = requests.put(url=Raspberry_url,headers=Raspberry_headers,data=data)

ReadServices = []
ReadServices.append(time_service())
ReadServices.append(temperature_service())
ReadServices.append(humidity_service())
ReadServices.append(smoke_service())
ReadServices.append(occupancy_service())
ReadServices.append(lamp_service_1())
ReadServices.append(lamp_service_2())
ReadServices.append(alarm_read_service())

ControlServices = []
ControlServices.append(alarm_control_service())
ControlServices.append(lamp_control_service_1)
ControlServices.append(lamp_control_service_2)

class trigger():

    def __init__(self, readserviceid, condition, value):
        self.read_service = ReadServices[readserviceid]
        self.condition = condition
        self.value = value
    
    def isTriggered(self):
        if(self.read_service.allowercondition==0):
            return self.read_service.get_value == self.value

class action():
    def __init__(self, controlserviceid, value):
        self.control_service = ControlServices[controlserviceid]
        self.value = value
    
    def act(self):
        self.control_service.set_value(self.value)


def SceneLoop(scenes = scene_dict[scenes]):
    for i in range(len(scenes)):
        tr = trigger(scenes[i]['trigger']['readserviceid'], scenes[i]['trigger']['condition'], scenes[i]['trigger']['value'])
        ac = action(scenes[i]['action']['controlserviceid'], scenes[i]['action']['value'])
        if(tr.isTriggered):
            ac.act()
        time.sleep(10)

if __name__ == '__main__':
    SceneLoop()