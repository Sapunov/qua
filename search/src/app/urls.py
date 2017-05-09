from django.conf.urls import url

from search import views


urlpatterns = [
    url(r'^search$', views.Search.as_view()),
    url(r'^index$', views.Index.as_view()),
    url(r'^items/(?P<item_id>[0-9a-z]{8})$', views.Items.as_view()),
]
