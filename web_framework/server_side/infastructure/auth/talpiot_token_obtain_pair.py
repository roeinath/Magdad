from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.settings import api_settings
# from rest_framework_simplejwt.serializers import login_rule, user_eligible_for_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase


class TalpiotTokenObtainPairSerializer(serializers.Serializer):
    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['token'] = serializers.CharField()

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        authenticate_kwargs = {
            'token': attrs['token'],
        }

        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None:
            print("Error - login invalid")
            return {}

        # if not getattr(login_rule, user_eligible_for_login)(self.user):
        #     raise exceptions.AuthenticationFailed(
        #         self.error_messages['no_active_account'],
        #         'no_active_account',
        #     )

        data = {}

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # TODO: Fix this
        # if api_settings.UPDATE_LAST_LOGIN:
        #     update_last_login(None, self.user)

        return data


class TalpiotTokenObtainPairView(TokenViewBase):
    serializer_class = TalpiotTokenObtainPairSerializer
