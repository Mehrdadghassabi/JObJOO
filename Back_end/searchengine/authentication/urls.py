from django.urls import path, re_path, include

from authentication.views import *

urlpatterns = [
    # path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('login-request/', LoginRequest.as_view(), name='login_request'),
    # re_path(
    #     'password/reset/(?P<username>\w+)?',
    #     ForgetPassword.as_view(),
    #     name='request_code'
    # ),
    # path(
    #     'check/password/',
    #     CheckTemplatePassword.as_view(),
    #     name='check_password'
    # ),
    path('profile/', Profile.as_view(), name='profile'),
    # path('', include('rest_auth.urls'))
]
