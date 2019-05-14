import requests
import time
import pymysql
import json
pymysql.install_as_MySQLdb()
import MySQLdb

dbnumber = MySQLdb.connect('localhost', 'root', '123456', 'home')           #连接本地数据库
cursor = dbnumber.cursor()
#r = requests.get('http://192.168.50.106:8080',timeout = 100)
#data = json.loads(r.text)
#insert_re = "insert into apps_info(temperature, humidity, occupancy, smoke) values (%s, %s, %s, %s)" % (data['temperature'],data['humidity'],data['occupancy'],data['smoke'])
#cursor.execute(insert_re)
dbnumber.commit()

while 1:
    try:
        r = requests.get('http://192.168.50.106:8080',timeout = 100)
    except:
        continue
    data = json.loads(r.text)
    insert_re = "UPDATE apps_info SET temperature=%s, humidity=%s, occupancy=%s, smoke=%s where id = 1" % (data['temperature'],data['humidity'],data['occupancy'],data['smoke'])
    cursor.execute(insert_re)
    dbnumber.commit()
    time.sleep(1)
dbnumber.close()             #最后关闭数据库连接
