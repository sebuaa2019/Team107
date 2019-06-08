from datetime import datetime

import requests
from .models import UpdateTime

'''
异常通知, 如果长时间收不到本地的请求, 就向用户通知家中可能出现了问题, 
报警信息不再可信
'''
URL = 'https://sc.ftqq.com/SCU37298T847874b7bf139ffb4081081f070bcbbc5c0bc8a6a0078.send'


def ExceptionDetect():
    info = {
        'text': 'AAA家庭报警装置提醒',
        'desp': '家中报警装置长时间无响应, 报警信息不可靠',
    }
    try:
        update_time = UpdateTime.objects.all()[0]
        time_interval = datetime.now() - update_time
        print("[{0}] last update time:{1}".format(datetime.now(), update_time))
        if time_interval.min > 10:
            requests.post(URL, data=info)
    except:
        print('Exception Detect Error!')

ExceptionDetect()
