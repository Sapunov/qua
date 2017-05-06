from django.conf.urls import url

from suggests import views


urlpatterns = [
    url(r'^accumulate$', views.Accumulate.as_view()),
    url(r'^suggest$', views.Suggest.as_view()),
]
