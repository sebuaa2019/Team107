import requests
import json
import time
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import sys
HB_url = 'http://localhost'

with open('/home/pi/Scripts/Services.json') as f:
    Service_dict = json.load(f)

class ReadService:
    def __init__(self, aid, iid):
        self.aid = aid
        self.iid = iid
        for i in range(len(Service_dict['readservices'])):
            if (Service_dict['readservices'][i]['aid']==aid and Service_dict['readservices'][i]['iid']==iid):
                self.allowercondition = Service_dict['readservices'][i]['allowed_condition']
        self.key = 'value'
    def get_value(self):
        if(self.aid == 0):
            if(self.iid == 0):
                localtime = time.localtime(time.time())
                return localtime.tm_hour+(localtime.tm_min/100)
        else:
            url = HB_url + ':39000/characteristics?id=' + str(self.aid) + '.' + str(self.iid)
            try:
                r = requests.get(url)
                di = json.loads(r.text)
                return di['characteristics'][0][self.key]
            except:
                print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "Service.py-ReadService: HomeBridge no Response")
        
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
            present_value = json.loads(requests.get(url = 'http://localhost:39000/characteristics?id=' + str(self.aid) + '.' + str(self.iid)).text)
            if(value != present_value['characteristics'][0]['value']):
                r = requests.put(url=Raspberry_url,headers=Raspberry_headers,data=data)
        except:
            dbnumber = MySQLdb.connect('localhost', 'root', '123456', 'home')  # 连接本地数据库
            cursor = dbnumber.cursor()
            dbnumber.commit()
            cursor.execute('select num  from apps_error where id = 1')
            result = cursor.fetchone()
            insert_re = "UPDATE apps_error SET num=%s where id = 1" % (result[0] + 1)
            cursor.execute(insert_re)
            dbnumber.commit()
            dbnumber.close()
            print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "Service.py-ControlService: HomeBridge no Response")
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
