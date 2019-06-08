from datetime import datetime
from .config import *
import requests
from . import models

'''
异常通知, 如果长时间收不到本地的请求, 就向用户通知家中可能出现了问题, 
报警信息不再可信
'''
def ExceptionDetect():
    info = {
        'text': 'AAA家庭报警装置提醒',
        'desp': '家中报警装置长时间无响应, 报警信息不可靠',
    }
    try:
        update_time = models.UpdateTime.objects.all()[0]
        time_interval = datetime.now() - update_time
        if time_interval.min > 10:
            requests.post(URL, data=info)
    except:
        print('Exception Detect Error!')