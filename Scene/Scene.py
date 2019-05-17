import time
import requests
import json

class ReadService():
    def __init__(self):
        self.id = 0
        self.aid = 0
        self.iid = 0
    
    def get_value(self):
        return 0

class ControlService():
    def __init__(self):
        self.id = 0
        self.aid = 0
        self.iid = 0
        self.key = '031-45-155'
    
    def set_value(self):
        return 0

class time_service(ReadService):
    def __init__(self):
        self.id = 0
        self.aid = 0
        self.iid = 0

    def get_value(self):
        localtime = time.localtime(time.time())
        return localtime.tm_hour+(localtime.tm_min/60)

class temperature_service(ReadService):
    def __init__(self):
        self.id = 1
        self.aid = 5
        self.iid = 10

    def get_value(self):
        r = requests.get('localhost:8000/sensor_db/')
        di = json.loads(r.text)
        return di["temperature"]

class humidity_service(ReadService):
    def __init__(self):
        self.id = 2
        self.aid = 5
        self.iid = 13

    def get_value(self):
        r = requests.get('localhost:8000/sensor_db/')
        di = json.loads(r.text)
        return di["humidity"]

class smoke_service(ReadService):
    def __init__(self):
        self.id = 3
        self.aid = 5
        self.iid = 19

    def get_value(self):
        r = requests.get('localhost:8000/sensor_db/')
        di = json.loads(r.text)
        return di["smoke"]

class occupancy_service(ReadService):
    def __init__(self):
        self.id = 4
        self.aid = 5
        self.iid = 25

    def get_value(self):
        r = requests.get('localhost:8000/sensor_db/')
        di = json.loads(r.text)
        return di["occupancy"]

class lamp_service_1(ReadService):
    def __init__(self):
        self.id = 5
        self.aid = 5
        self.iid = 25

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

def setup():
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

def SceneLoop():
    with open(./)