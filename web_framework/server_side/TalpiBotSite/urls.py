"""TalpiBotSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from web_framework.server_side.infastructure.auth.talpiot_token_obtain_pair import TalpiotTokenObtainPairView
from web_framework.server_side.infastructure.auth.user_view import UserGetView
from web_framework.server_side.infastructure.request_handlers import *

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    path('run_func/', run_func, name='run_func'),
    path('get_file/', get_file, name='get_file'),
    path('get_page/', get_page, name='get_page'),
    path('get_data/', get_data, name='get_data'),
    path('get_page_list/', get_pages, name='get_pages'),
    path('quick_access_pages/', quick_access_pages, name='quick_access_pages'),
    path('get_data/', get_data, name='get_data'),
    # path('main/', include('web_framework.server_side.main.urls')),
    # path('', include('web_framework.server_side.main.urls')),
    path('api/token/', TalpiotTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/user/get/', UserGetView.as_view(), name='token_user_get'),
    path('api/get_ynet_news/', get_ynet_news, name = 'get_ynet_news'),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login')
]

