from django.conf.urls import url

from qua.api import views
from qua.api.views import obtain_jwt_token


urlpatterns = [
    url(r'^search$', views.SearchView.as_view()),
    url(r'^questions$', views.QuestionListView.as_view()),
    url(r'^questions/(?P<question_id>[0-9]{1,10})$', views.QuestionView.as_view(), name='api-question'),
    url(r'^categories$', views.CategoryListView.as_view()),
    url(r'^categories/(?P<category_id>[0-9]{1,10})$', views.CategoryView.as_view()),
    # url(r'^categories/search$', views.CategoriesSearchView.as_view()),
    # url(r'^keywords/search$', views.KeywordsSearchView.as_view()),
    url(r'^auth$', obtain_jwt_token),
]
