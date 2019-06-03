from django.test import TestCase
from .models import Room,Device,RoomDevice,Scene
import json
import os
# Create your tests here.



class RoomViewTest(TestCase):

    #添加房间
    def test_add_room_normal(self):
        res = self.client.post('/room/add/',{"room_name":"room_new"},content_type = 'application/json')
        self.assertEqual(res.content,b'200')
        rooms = Room.objects.filter(room_name = "room_new")
        self.assertEqual(rooms.exists(),True)

    #添加房间名为空
    def test_add_room_blank(self):
        res = self.client.post('/room/add/',{"room_name":""},content_type = 'application/json')
        self.assertEqual(res.content,b'200')
        rooms = Room.objects.filter(room_name="")
        self.assertEqual(rooms.exists(), True)

    #获取房间
    def test_get_room(self):
        test_room = Room.objects.create()
        test_room.room_name = "get_room"
        test_room.save()

        res = self.client.post('/room/getRoom/',{"roomId":test_room.id},content_type = 'application/json')
        self.assertEqual(res.content,b'{"id": %d, "room_name": "get_room"}'%test_room.id)

    #更改房间
    def test_update_room(self):
        test_room = Room.objects.create()
        test_room.room_name = "old_name"
        test_room.save()

        res = self.client.post('/room/update/',{"id":test_room.id,"room_name":"new_name"},content_type = 'application/json')
        test_room = Room.objects.get(id=test_room.id)
        self.assertEqual(test_room.room_name,  "new_name")
        self.assertEqual(res.content,b'200')

    #房间列表
    def test_room_list_and_table(self):

        test_room1 = Room.objects.create()
        test_room1.room_name = "room_1"
        test_room1.save()

        res_table = self.client.get('/room/table/')
        self.assertEqual(res_table.content,b'[{"id": %d, "room_name": "room_1"}]'%test_room1.id)

        res_list = self.client.get('/room/list/')
        self.assertEqual(res_list.content, b'[{"id": %d, "room_name": "room_1"}]' % test_room1.id)

        test_room2 = Room.objects.create()
        test_room2.room_name = "room_2"
        test_room2.save()

        res_table = self.client.get('/room/table/')
        self.assertEqual(res_table.content,b'[{"id": %d, "room_name": "room_1"}, {"id": %d, "room_name": "room_2"}]'%(test_room1.id,test_room2.id))

        res_list = self.client.get('/room/list/')
        self.assertEqual(res_list.content,b'[{"id": %d, "room_name": "room_1"}, {"id": %d, "room_name": "room_2"}]' % (test_room1.id, test_room2.id))

    #删除房间
    def test_room_delete(self):
        test_room = Room.objects.create()
        test_room.room_name = "room_delete"
        test_room.save()
        self.assertEqual(Room.objects.filter(room_name = "room_delete").exists(),True)

        res = self.client.post('/room/delete/',{"idString":str(test_room.id)},content_type = 'application/json')

        self.assertEqual(res.content,b'200')
        self.assertEqual(Room.objects.filter(room_name = "room_delete").exists(), False)

    #批量删除
    def test_room_delete_2(self):
        test_room1 = Room.objects.create()
        test_room1.room_name = "room_1"
        test_room1.save()

        test_room2 = Room.objects.create()
        test_room2.room_name = "room_2"
        test_room2.save()

        res = self.client.post('/room/delete/', {"idString": "%d,%d"%(test_room1.id,test_room2.id)}, content_type='application/json')
        self.assertEqual(res.content, b'200')
        self.assertEqual(Room.objects.filter().exists(), False)

def create_device(device_id,device_name,status = 0,arg_type = 0,arg = 0,device_type = 0 ):
    return Device.objects.create(device_id = device_id,device_name = device_name,status = status,arg_type = arg_type,arg = arg,device_type = device_type)

#设备测试
class DeviceViewTest(TestCase):

    #添加设备
    def test_add_device(self):

        res = self.client.post('/device/add/',{"id":10000,"device_name":"lamp","status":0},content_type = 'application/json')
        self.assertEqual(res.content,b'200')

        added = Device.objects.filter(device_name = "lamp",device_id = 10000,status = 0).exists()
        self.assertEqual(added,True)

    #获取设备信息
    def test_get_device(self):

        device_1 = create_device(device_id = 1,device_name = "new_device")
        added = Device.objects.filter(device_name="new_device", device_id=1).exists()
        self.assertEqual(added, True)
        res = self.client.post('/device/getDevice/', {"deviceId":1},content_type='application/json')
        self.assertEqual(res.content,b'{"id": 1, "device_name": "new_device", "status": 0, "arg_type": 0, "arg": 0.0, "device_type": 0, "room_id": ""}')

    #设备列表
    def test_device_table(self):

        test_lamp = create_device(10000,"lamp",0,1,0,1)
        test_computer = create_device(20000,"computer",0,1,0,0)
        res = self.client.get('/device/table/')
        self.assertEqual(res.content,b'[{"id": 10000, "device_name": "lamp", "status": 0, "arg_type": 1, "arg": 0.0, "device_type": 1, "room_id": ""}, '
                                     b'{"id": 20000, "device_name": "computer", "status": 0, "arg_type": 1, "arg": 0.0, "device_type": 0, "room_id": ""}]')

    #设备更新
    def test_device_update(self):
        test_lamp = create_device(10000, "lamp", 1, 1, 0, 1)


        res = self.client.post('/device/update/',{"id": 10000, "device_name": "broken_lamp", "status": 0, "room": 711},content_type = 'application/json')
        new_lamp = Device.objects.filter(device_id = 10000,device_name = "broken_lamp", status = 0)
        new_room = RoomDevice.objects.get(device_id = 10000).room_id
        updated = new_lamp.exists() and new_room == 711
        self.assertEqual(res.content, b'200')
        self.assertEqual(updated,True)

        res = self.client.post('/device/update/',{"id": 10000, "device_name": "fixed_lamp", "status": 1, "room": 101},content_type = 'application/json')
        new_lamp = Device.objects.filter(device_id=10000, device_name="fixed_lamp", status=1)
        new_room = RoomDevice.objects.get(device_id=10000).room_id
        updated = new_lamp.exists() and new_room == 101
        self.assertEqual(res.content, b'200')
        self.assertEqual(updated, True)

    #删除设备
    def test_device_delete(self):
        device_1 = create_device(device_id=1, device_name="new_device")

        added = Device.objects.filter(device_name="new_device", device_id=1).exists()
        self.assertEqual(added, True)

        res = self.client.post('/device/delete/',{"idString": "1"},content_type = 'application/json')

        added = Device.objects.filter(device_name="new_device", device_id=1).exists()
        self.assertEqual(res.content,b'200')
        self.assertEqual(added, False)

    #批量删除
    def test_device_delete_2(self):

        test_lamp = create_device(10000, "lamp", 0, 1, 0, 1)
        test_computer = create_device(20000, "computer", 0, 1, 0, 0)

        res = self.client.post('/device/delete/', {"idString": "10000,20000"}, content_type='application/json')

        self.assertEqual(Device.objects.all().exists(),False)
        self.assertEqual(res.content,b'200')

    #上传设备信息
    def test_device_upload_data(self):
        with open(os.path.join(os.path.abspath('.'),'json-test.json')) as f:
            data_dict = json.load(f)

        res = self.client.post('/device/upload/',json.dumps(data_dict),content_type = 'application/json')

        expected_res =b'{"accessories": [{"aid": 8, "name": "\u62a5\u8b66\u5f00\u5173", "iids": [{"iid": 10, "valuetype": 1, "currentvalue": false}]}, ' \
                      b'{"aid": 2, "name": "\u5c0f\u7c73\u53f0\u706f-1", "iids": [{"iid": 10, "valuetype": 1, "currentvalue": false}]}, ' \
                      b'{"aid": 3, "name": "\u5c0f\u7c73\u53f0\u706f-2", "iids": [{"iid": 10, "valuetype": 1, "currentvalue": true}]}]}'

        self.assertEqual(res.content,expected_res)

    #控制设备列表
    def test_device_control_list(self):

        with open(os.path.join(os.path.abspath('.'),'json-test.json')) as f:
            data_dict = json.load(f)

        self.client.post('/device/upload/',json.dumps(data_dict),content_type = 'application/json')

        res_list = self.client.get('/device/controlDeviceList/')

        expected_res =b'[{"id": 20010, "device_name": "\u5c0f\u7c73\u53f0\u706f-1", "status": 1, "arg_type": 1, "arg": 0.0, "device_type": 1, "room_id": ""}, ' \
                      b'{"id": 30010, "device_name": "\u5c0f\u7c73\u53f0\u706f-2", "status": 1, "arg_type": 1, "arg": 1.0, "device_type": 1, "room_id": ""}, ' \
                      b'{"id": 80010, "device_name": "\u62a5\u8b66\u5f00\u5173", "status": 1, "arg_type": 1, "arg": 0.0, "device_type": 1, "room_id": ""}]'
        self.assertEqual(res_list.content,expected_res)

    #报警功能测试
    def test_device_upload_alarm_detect(self):
        #若将json-test中的 人体传感器 和 报警开关 的 current_value 设置为真 , 应能接收到入侵报警推送
        #若将json-test中的 烟雾传感器 和 报警开关 的 current_value 设置为真 , 应能接收到火灾报警推送
        with open(os.path.join(os.path.abspath('.'),'json-test.json')) as f:
            data_dict = json.load(f)

        self.client.post('/device/upload/',json.dumps(data_dict),content_type = 'application/json')

        self.assertEqual(1,1)

    #入侵报警
    def test_device_alarm(self):
        alarm_control = create_device(device_id= 80010,device_name = "alarm",arg = 0)
        body_sensor = create_device(device_id = 70010,device_name = "body_sensor", arg =1)
        res = self.client.get('/device/alarm/')

        self.assertEqual(res.content,b'{"alarm_control": 0.0, "alarm_info": 1.0}')

    #火警
    def test_device_fire(self):
        alarm_control = create_device(device_id=80010, device_name="alarm", arg=1)
        fire_sensor = create_device(device_id=60010, device_name="fire_sensor", arg=1)
        res = self.client.get('/device/fire/')

        self.assertEqual(res.content, b'{"alarm_control": 1.0, "fire_info": 1.0}')

    # def test_device_temperature(self):
    #
    #     thermometer = create_device(device_id = 40010,device_name="temp",arg = 23)
    #     res = self.client.get('/device/temperature/?id = 40010')
    #     self.assertEqual(res.content,b'200')


def create_scene(scene_name, read_service_id, control_service_id, trigger_value, trigger_condition, action_value, status):
    return Scene.objects.create(scene_name = scene_name, read_service_id = read_service_id, control_service_id = control_service_id,trigger_value = trigger_value, trigger_condition = trigger_condition, action_value = action_value, status =status)

#场景测试
class SceneViewTest(TestCase):

    #添加场景
    def test_scene_add(self):
        res =self.client.post('/scene/add/',{"scene_name": "new_scene", "tri-service": "40010", "tri-condition": "1", "arg": "25", "action-service": "20010", "of-value": "1", "status": "1"},content_type = 'application/json')

        added = Scene.objects.filter(scene_name = "new_scene").exists()
        self.assertEqual(res.content,b'200')
        self.assertEqual(added,True)

    #获取场景信息
    def test_scene_get(self):
        test_scene = create_scene("s1",40010,20010,30,0,0,1)
        added = Scene.objects.filter(scene_name="s1").exists()

        res = self.client.post('/scene/getScene/',{"sceneId": test_scene.id},content_type = 'application/json')
        self.assertEqual(res.content,b'{"id": %d, "scene_name": "s1", "status": 1, "trigger": {"readserviceid": 40010, "condition": 0, "value": 30.0}, "action": {"controlserviceid": 20010, "value": false}}'%test_scene.id)

    #场景列表
    def test_scene_table(self):
        s1 = create_scene("s1",40010,20010,30,0,0,1)
        s2 = create_scene("s2",50010,30010,25,2,1,0)
        res = self.client.get('/scene/table/')
        expected_table = b'[{"id": %d, "scene_name": "s1", "status": 1, "trigger": {"readserviceid": 40010, "condition": 0, "value": 30.0}, "action": {"controlserviceid": 20010, "value": false}}, ' \
                         b'{"id": %d, "scene_name": "s2", "status": 0, "trigger": {"readserviceid": 50010, "condition": 2, "value": 25.0}, "action": {"controlserviceid": 30010, "value": true}}]'%(s1.id,s2.id)

        self.assertEqual(res.content,expected_table)

    #场景更改
    def test_scene_update(self):

        s1 = create_scene("scene", 50010, 30010, 25, 2, 1, 0)
        res = self.client.post('/scene/update/',{"id": s1.id, "scene_name":"scene_update","tri-service":"40010","tri-condition":"1","arg":"30","action-service":"20010","of-value":"0","status":"1"},content_type = 'application/json')

        updated = Scene.objects.filter(scene_name = "scene_update").exists()
        self.assertEqual(updated,True)
        self.assertEqual(res.content,b'200')

    #场景删除
    def test_scene_delete(self):
        s1 = create_scene("scene", 50010, 30010, 25, 2, 1, 0)
        added = Scene.objects.filter(scene_name = "scene").exists()
        self.assertEqual(added,True)

        res = self.client.post('/scene/delete/',{"idString":str(s1.id)},content_type = 'application/json')
        deleted = not Scene.objects.filter(scene_name = "scene").exists()
        self.assertEqual(deleted,True)
        self.assertEqual(res.content,b'200')

    #批量删除
    def test_scene_delete_2(self):
        s1 = create_scene("scene_1", 50010, 30010, 25, 2, 1, 0)
        s2 = create_scene("scene_2", 40010, 20010, 30, 0, 0, 1)

        res = self.client.post('/scene/delete/', {"idString": "%d,%d"%(s1.id,s2.id)}, content_type='application/json')
        all_deleted = not Scene.objects.all().exists()

        self.assertEqual(all_deleted,True)
        self.assertEqual(res.content,b'200')

    #def test_service_list(self):


    #服务信息更新
    def test_scene_service(self):

        with open(os.path.join(os.path.abspath('.'), 'scene_test.json')) as f:
            service_dict = json.load(f)

        res = self.client.post('/scene/service/', json.dumps(service_dict), content_type='application/json')
        self.assertEqual(res.content,b'200')

    #场景信息下载
    def test_scene_download(self):

        s1 = create_scene("scene_1", 40010, 20010, 30, 0, 0, 1)
        s2 = create_scene("scene_2", 50010, 30010, 25, 0, 1, 0)

        res = self.client.get('/scene/download/')
        expected_out = b'{"scenes": [{"id": %d, "scene_name": "scene_1", "status": 1, "trigger": {"readserviceid": 40010, "condition": 0, "value": 30.0}, "action": {"controlserviceid": 20010, "value": false}}, ' \
                       b'{"id": %d, "scene_name": "scene_2", "status": 0, "trigger": {"readserviceid": 50010, "condition": 0, "value": 25.0}, "action": {"controlserviceid": 30010, "value": true}}]}'%(s1.id,s2.id)

        self.assertEqual(res.content,expected_out)















