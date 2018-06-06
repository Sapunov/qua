from django.conf.urls import url

from api import views


urlpatterns = [
    # auth
    url(r'^auth$', views.obtain_jwt_token),
    url(r'^token-verify$', views.verify_jwt_token),

    # search
    url(r'^search$', views.SearchView.as_view()),

    # questions
    url(r'^questions$', views.QuestionListView.as_view()),
    url(r'^questions/(?P<question_id>[0-9]{1,10})$',
        views.QuestionView.as_view(),
        name='api-question'),

    # external
    url(r'^external$', views.ExtResources.as_view()),
    url(r'^external/(?P<external_id>[0-9]{1,10})$',
        views.ExtResource.as_view()),
    url(r'^external/bulk$', views.ExtResourceBulk.as_view()),
]
