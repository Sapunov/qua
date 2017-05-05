from django.conf.urls import url

from suggests import views


urlpatterns = [
    url(r'^/api/accumulate$', views.Accumulate.as_view()),
    url(r'^/api/suggest$', views.Suggest.as_view()),
]
