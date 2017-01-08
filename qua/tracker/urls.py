from django.conf.urls import url

from qua.tracker import views


urlpatterns = [
    url(r'^search$', views.search_tracker, name='tracker-search'),
]
