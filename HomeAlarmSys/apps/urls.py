from django.conf.urls import url, include 

from apps import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
]