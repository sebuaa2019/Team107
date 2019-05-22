from django.conf.urls import url, include 

from .view import views
from .view import scene
from .view import room
from .view import device

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    #url(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    url(r'index/', views.index, name='index'),

    url(r'login/', views.login, name='login'),
    url(r'register/', views.register, name='register'),
    url(r'logout/', views.logout, name='logout'),

    url(r'profile/', views.profile, name='profile'),
    url(r'editProfile/', views.edit, name='editProfile'),

    url(r'user/manage/', views.user_manage, name='user_manage'),
    url(r'user/table/', views.user_table, name='user_table'),

    url(r'room/manage/', room.room_manage, name='room_manage'),
    url(r'room/table/', room.room_table, name='room_table'),
    url(r'room/add/', room.room_add, name='room_add'),
    url(r'room/getRoom/', room.room_get, name='room_get'),
    url(r'room/update/', room.room_update, name='room_update'),
    url(r'room/delete/', room.room_delete, name='room_delete'),
    url(r'room/list/', room.room_list, name='room_list'),


    url(r'scene/manage/', scene.scene_manage, name='scene_manage'),
    url(r'scene/table/', scene.scene_table, name='scene_table'),
    url(r'scene/add/', scene.scene_add, name='scene_add'),
    url(r'scene/getScene/', scene.scene_get, name='scene_get'),
    url(r'scene/update/', scene.scene_update, name='scene_update'),
    url(r'scene/delete/', scene.scene_delete, name='scene_delete'),
    url(r'scene/service/', scene.scene_service, name='scene_service'),
    url(r'scene/download/', scene.scene_download, name='scene_download'),
    url(r'scene/serviceList/', scene.service_list, name='service_list'),


    url(r'device/manage/', device.device_manage, name='device_manage'),
    url(r'device/table/', device.device_table, name='device_table'),
    url(r'device/add/', device.device_add, name='device_add'),
    url(r'device/getDevice/', device.device_get, name='device_get'),
    url(r'device/update/', device.device_update, name='device_update'),
    url(r'device/delete/', device.device_delete, name='device_delete'),
    url(r'device/upload/', device.device_upload, name='device_upload'),
    url(r'device/on_off/', device.device_on_off, name='device_on_off'),
    url(r'device/alarm/', device.device_alarm, name='device_alarm'),
    url(r'device/smoke/', device.device_smoke, name='device_smoke'),
    url(r'device/fire/', device.device_fire, name='device_fire'),
    url(r'device/controlDeviceList/', device.control_device_list, name='device_control_list'),


    url(r'device/alarm/', device.device_alarm, name='device_alarm'),
    url(r'device/fire/', device.device_fire, name='device_fire'),
    url(r'device/smoke/', device.device_smoke, name='device_smoke'),



    url('^$', views.index, name='index'),
]
