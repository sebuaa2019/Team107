import requests
import time

while 1:
    r = requests.get('http://192.168.50.106:8080',timeout = 100)
    print(r.text)
    time.sleep(1)