#!/bin/bash

python3 /home/pi/AlarmSysLocal/get_data.py &
pid = `ps -ef|grep get_data.py | grep -v grep | awk '{print $2}'`

python3 /home/pi/AlarmSysLocal/manage.py runserver 0.0.0.0:8000 &
DEBUG=* homebridge -D -P home/pi/plugin_test/homebridge-httpalarm/ -I &