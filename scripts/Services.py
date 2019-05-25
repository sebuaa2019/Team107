import requests
import json
import time

HB_url = 'http://localhost'

class ReadService:
    def __init__(self, aid, iid):
        self.aid = aid
        self.iid = iid
        self.allowercondition = 0
        self.key = 'value'
    def get_value(self):
        if(self.aid == 0):
            if(self.iid == 0):
                localtime = time.localtime(time.time())
                return localtime.tm_hour+(localtime.tm_min/100)
        else:
            url = HB_url + ':39000/characteristics?id=' + str(self.aid) + '.' + str(self.iid)
            r = requests.get(url)
            di = json.loads(r.text)
            return di['characteristics'][0][self.key]
        
class ControlService:
    def __init__(self, aid, iid):
        self.aid = aid
        self.iid = iid
        self.key = '031-45-155'
        self.allowedvalue = 0
    def set_value(self, value):
        Raspberry_headers = {'authorization': self.key}
        Raspberry_url = HB_url + ':39000/characteristics' 
        data = '{\"characteristics\":[{\"aid\":' + str(self.aid) + ',\"iid\":' + str(self.iid) + ',\"value\":' + str(value).lower() + ',\"status\":0}]}'
        try:
            r = requests.put(url=Raspberry_url,headers=Raspberry_headers,data=data)
        except:
            print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "Service.py: HomeBridge not Response")
            return -1
        return True

class time_service(ReadService):
    def __init__(self):
        self.id = 0
        self.aid = 0
        self.iid = 0
        self.allowercondition = 0

class temperature_service(ReadService):
    def __init__(self):
        self.id = 1
        self.aid = 5
        self.iid = 10
        self.allowercondition = 1
        self.key = "value"

class humidity_service(ReadService):
    def __init__(self):
        self.id = 2
        self.aid = 5
        self.iid = 13
        self.allowercondition = 1
        self.key = "value"

class smoke_service(ReadService):
    def __init__(self):
        self.id = 3
        self.aid = 5
        self.iid = 19
        self.allowercondition = 0
        self.key = "value"

class occupancy_service(ReadService):
    def __init__(self):
        self.id = 4
        self.aid = 5
        self.iid = 25
        self.allowercondition = 0
        self.key = "value"

class lamp_service_1(ReadService):
    def __init__(self):
        self.id = 5
        self.aid = 8
        self.iid = 10
        self.allowercondition = 0
        self.key = "value"

class lamp_service_2(ReadService):
    def __init__(self):
        self.id = 6
        self.aid = 9
        self.iid = 10
        self.allowercondition = 0
        self.key = "value"

class alarm_read_service(ReadService):
    def __init__(self):
        self.id = 7
        self.aid = 7
        self.iid = 10
        self.allowercondition = 0
        self.key = "value"

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
