import requests
import json
import time

HB_url = 'http://localhost'

class ReadService():
    def __init__(self):
        self.id = 0
        self.aid = 0
        self.iid = 0
        self.allowercondition = 0
        self.key = ''
    
    def get_value(self):
        try:
            r = requests.get(HB_url + ':8000/sensor_db/')
            di = json.loads(r.text)
            return di[self.key]
        except:
            print("Local Django not Response")
            return 0
        
class ControlService():
    id = 0
    aid = 0
    iid = 0
    key = '031-45-155'
    allowedvalue = 0
    def __init__(self):
        pass
    def set_value(self, value):
        Raspberry_headers = {'authorization': self.key}
        Raspberry_url = HB_url + ':39000/characteristics' 
        data = '{\"characteristics\":[{\"aid\":' + str(self.aid) + ',\"iid\":' + str(self.iid) + ',\"value\":' + str(value).lower() + ',\"status\":0}]}'
        try:
            r = requests.put(url=Raspberry_url,headers=Raspberry_headers,data=data)
        except:
            print("HomeBridge not Response")
            return -1
        return True

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
        self.key = "temperature"

class humidity_service(ReadService):
    def __init__(self):
        self.id = 2
        self.aid = 5
        self.iid = 13
        self.allowercondition = 1
        self.key = "humidity"

class smoke_service(ReadService):
    def __init__(self):
        self.id = 3
        self.aid = 5
        self.iid = 19
        self.allowercondition = 0
        self.key = "smoke"

class occupancy_service(ReadService):
    def __init__(self):
        self.id = 4
        self.aid = 5
        self.iid = 25
        self.allowercondition = 0
        self.key = "occupancy"

class lamp_service_1(ReadService):
    def __init__(self):
        self.id = 5
        self.aid = 8
        self.iid = 10
        self.allowercondition = 0
        self.key = "value"

    def get_value(self):
        url = HB_url + ':39000/characteristics?id=' + str(self.aid) + '.' + str(self.iid)
        r = requests.get(url)
        di = json.loads(r.text)
        return di['characteristics'][0][self.key]

class lamp_service_2(ReadService):
    def __init__(self):
        self.id = 6
        self.aid = 9
        self.iid = 10
        self.allowercondition = 0
        self.key = "value"

    def get_value(self):
        url = HB_url + ':39000/characteristics?id=' + str(self.aid) + '.' + str(self.iid)
        r = requests.get(url)
        di = json.loads(r.text)
        return di['characteristics'][0][self.key]

class alarm_read_service(ReadService):
    def __init__(self):
        self.id = 7
        self.aid = 7
        self.iid = 10
        self.allowercondition = 0
        self.key = "value"

    def get_value(self):
        url = HB_url + ':39000/characteristics?id=' + str(self.aid) + '.' + str(self.iid)
        r = requests.get(url)
        di = json.loads(r.text)
        return di['characteristics'][0][self.key]

class alarm_control_service(ControlService):
    def __init__(self):
        self.id = 0
        self.aid = 7
        self.iid = 10

class lamp_control_service_1(ControlService):
    def __init__(self):
        self.id = 1
        self.aid = 8
        self.iid = 10

class lamp_control_service_2(ControlService):
    def __init__(self):
        self.id = 2
        self.aid = 9
        self.iid = 10
