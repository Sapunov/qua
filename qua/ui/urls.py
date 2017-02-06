from django.conf.urls import url

from qua.ui import views


urlpatterns = [
    url(r'^password_reset/(?P<user_id>[0-9]{1,10})$', views.password_reset, name='password_reset'),
    url(r'^', views.index),
]
