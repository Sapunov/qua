from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token

from qua.api import views


urlpatterns = [
    url(r'^search$', views.SearchView.as_view()),
    url(r'^questions$', views.QuestionsListView.as_view()),
    url(r'^questions/(?P<question_id>[0-9]{1,10})$', views.QuestionsDetailView.as_view()),
    url(r'^categories$', views.CategoriesListView.as_view()),
    url(r'^categories/(?P<category_id>[0-9]{1,10})$', views.CategoriesDetailView.as_view()),
    url(r'^auth$', obtain_jwt_token),
]
