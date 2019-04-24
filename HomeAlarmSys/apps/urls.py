from django.conf.urls import url, include 

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^logout/', views.logout,name='logout'),
    url(r'^edit/', views.edit,name='edit'),
    url(r'^captcha', include('captcha.urls'))
]