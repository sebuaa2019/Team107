import requests
import time
import pymysql
import json
pymysql.install_as_MySQLdb()
import MySQLdb
import sys
import serial
import re
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
i = 0
while (i<=25):
    response = ser.readall().decode()
    result = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', response)
    if(result):
        print(result[0])
        break
    i = i+1
dbnumber = MySQLdb.connect('localhost', 'root', '123456', 'home')           #连接本地数据库
cursor = dbnumber.cursor()
#r = requests.get('http://192.168.50.106:8080',timeout = 100)
#data = json.loads(r.text)
#insert_re = "insert into apps_info(temperature, humidity, occupancy, smoke) values (%s, %s, %s, %s)" % (data['temperature'],data['humidity'],data['occupancy'],data['smoke'])
#cursor.execute(insert_re)
dbnumber.commit()

while 1:
    try:
        r = requests.get('http://' + str(result[0]) + ':8080',timeout = 100)
        data = json.loads(r.text)
        insert_re = "UPDATE apps_info SET temperature=%s, humidity=%s, occupancy=%s, smoke=%s where id = 1" % (data['temperature'],data['humidity'],data['occupancy'],data['smoke'])
        cursor.execute(insert_re)
        dbnumber.commit()
        time.sleep(1)
    except:
        cursor.execute('select num  from apps_error where id = 1')
        result = cursor.fetchone()
        insert_re = "UPDATE apps_error SET num=%s where id = 1" % (result[0]+1)
        cursor.execute(insert_re)
        dbnumber.commit()
        print(str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + ':' + str(time.localtime().tm_sec) + "    " + "GetFromArduino.py: Arduino no Response")
        time.sleep(30)
dbnumber.close()             #最后关闭数据库连接
