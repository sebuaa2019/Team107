from django.conf.urls import url, include 

from . import views
'''
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^logout/', views.logout,name='logout'),
    url(r'^edit/', views.edit,name='edit'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^captcha', include('captcha.urls'))
]
'''


urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    #url(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page

    url(r'login/', views.login, name='login'),
    url(r'index/', views.index, name='index'),
    url(r'register/', views.register, name='register'),
    url(r'logout/', views.logout, name='logout'),

    url('^$', views.index, name='index'),
]
