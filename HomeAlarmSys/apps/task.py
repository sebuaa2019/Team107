from datetime import datetime, timedelta
import requests
from .models import UpdateTime

URL = 'https://sc.ftqq.com/SCU37298T847874b7bf139ffb4081081f070bcbbc5c0bc8a6a0078.send'


def ExceptionDetect():
    info = {
        'text': 'AAA家庭报警装置提醒',
        'desp': '家中报警装置长时间无响应, 报警信息不可靠',
    }
    try:
        update_time = UpdateTime.objects.all()[0].update_time
        time_interval = datetime.now() - update_time
        print("[{0}] last update time:{1}".format(datetime.now(), update_time))
        print(time_interval)
        if time_interval > timedelta(minutes=10):
            requests.post(URL, data=info)
    except Exception as e:
        print(e)