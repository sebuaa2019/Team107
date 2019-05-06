from django.conf.urls import url, include 

from . import views
from . import scene


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

    url(r'room/manage/', views.room_manage, name='room_manage'),
    url(r'room/table/', views.room_table, name='room_table'),
    url(r'room/add/', views.room_add, name='room_add'),

    url(r'scene/manage/', scene.scene_manage, name='scene_manage'),
    url(r'scene/table/', scene.scene_table, name='scene_table'),
    url(r'scene/add/', scene.scene_add, name='scene_add'),
    url(r'scene/getScene/', scene.scene_get, name='scene_get'),
    url(r'scene/update/', scene.scene_update, name='scene_update'),
    url(r'scene/delete/', scene.scene_delete, name='scene_delete'),

    url('^$', views.index, name='index'),
]
