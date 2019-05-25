#!/bin/bash
ps -ef | grep python3 | cut -c 9-15| xargs kill -s 9
ps -ef | grep homebridge | cut -c 9-15| xargs kill -s 9
echo "Kill Complete"
python3 /home/pi/Scripts/GetFromArduino.py 192.168.50.106 &
sleep 3
echo "GetFromArduino.py Started"
python3 /home/pi/AlarmSysLocal/manage.py runserver 0.0.0.0:8000 >django.log 2>&1 &
sleep 7
echo "Django Started"
DEBUG=* homebridge -D -P /home/pi/plugin_test/homebridge-httpalarm/ -I >hombridge.log 2>&1 &
sleep 20
echo "homebridge Started"
python3 ./Scripts/Initiate.py
echo "Devices.json, Scenes.json and Services.json complete initializing"
python3 /home/pi/Scripts/DataToServer.py &
sleep 5
echo "DataToServer.py Started"
python3 /home/pi/Scripts/Scene.py >scenes.log 2>&1 &
echo "Scene.py Started"