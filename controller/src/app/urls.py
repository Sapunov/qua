from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from passport import views as passport_views


urlpatterns = [
    path('users', passport_views.UserView.as_view(), name='users'),
    path('users/email_exists', passport_views.EmailExistsView.as_view(), name='email_exists'),
    path('users/username_exists', passport_views.UsernameExistsView.as_view(), name='username_exists'),
    path('password/set', passport_views.SetPasswordView.as_view(), name='password_set'),
    path('password/obtain_reset_token', passport_views.ObtainResetTokenView.as_view(), name='obtain_reset_token'),
    path('sessions', passport_views.UserSessionsView.as_view(), name='user_sessions'),
    path('sessions/obtain_access_token', passport_views.ObtainAccessTokenView.as_view(), name='obtain_access_token'),
    path('sessions/<str:session_id>', passport_views.IndividualUserSessionView.as_view(), name='individual_user_session')
]

if settings.ADMIN_ENABLED:
    urlpatterns.insert(0, path('admin/', admin.site.urls))
