from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^api/', include('qua.api.urls')),
    url(r'^clck/', include('qua.tracker.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('qua.wi.urls')),
]
