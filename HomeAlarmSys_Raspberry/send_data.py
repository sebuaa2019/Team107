import requests
import time
import pymysql
import json
pymysql.install_as_MySQLdb()
import MySQLdb
server_error_url = 'http://39.106.138.175/error/notify/'
headers = {'Content-Type': 'application/json'}

dbnumber = MySQLdb.connect('localhost', 'root', '123456', 'home')           #连接本地数据库
cursor = dbnumber.cursor()
dbnumber.commit()

while 1:
    cursor.execute('select num  from apps_error where id = 1')
    result = cursor.fetchone()
    error_dict = {'num': result[0]}
    requests.post(url=server_error_url, headers=headers, data=json.dumps(error_dict))
    time.sleep(1)
dbnumber.close()             #最后关闭数据库连接
