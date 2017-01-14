from django.conf.urls import url

from qua.ui import views


urlpatterns = [
    url(r'^$', views.index),
]
