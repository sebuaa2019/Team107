
from django.conf.urls import url, include 
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app/', include('apps.urls')),
    url(r'^', include('apps.urls')),
]
