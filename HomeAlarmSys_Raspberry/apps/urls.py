from django.conf.urls import url, include 

from . import views

urlpatterns = [
    url(r'^$',views.index,name = 'home'),
    url(r'index/',views.index,name = 'index'),
    url(r'sensor/', views.sensor, name = 'sensor'),
    url(r'accessory/', views.accessory, name = 'accessory'),
    url(r'alarm/', views.alarm, name = 'alarm'),
    url(r'alarm_switch_on/', views.switch_on, name = 'switch'),
    url(r'alarm_switch_off/', views.switch_off, name = 'switch1'),
    url(r'sensor_db/',views.sensor_db, name = 'send_data'),
]
