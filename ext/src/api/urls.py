from django.conf.urls import url

from api import views


urlpatterns = [
    url(r'^search$', views.SearchView.as_view()),
    url(r'^questions$', views.QuestionListView.as_view()),
    url(r'^questions/(?P<question_id>[0-9]{1,10})$',
        views.QuestionView.as_view(),
        name='api-question'),
    url(r'^auth$', views.obtain_jwt_token),
    url(r'^token-verify$', views.verify_jwt_token),
    url(r'^extresources$', views.ExtResources.as_view()),
    url(r'^extresources/(?P<extresource_id>[0-9]{1,10})$',
        views.ExtResource.as_view()),
    url(r'^extresources/bulk$', views.ExtResourceBulk.as_view()),
]
