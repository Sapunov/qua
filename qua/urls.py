from django.conf.urls import url, include
from django.contrib import admin

from qua.api.views.away import AwayView


urlpatterns = [
    url(r'^api/', include('qua.api.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^away$', AwayView.as_view(), name='away'),
    url(r'^', include('qua.ui.urls')),
]
