from django.contrib.auth.backends import BaseBackend
from google.auth.transport import requests
from google.oauth2 import id_token

from APIs.TalpiotAPIs import User


class GoogleAuthenticationBackend(BaseBackend):
    """
    The client ID for TalpiBot (issued by Google).
    """
    CLIENT_ID = "330244991572-iimj6mtoao2motr1c05oklic54oo50vb.apps.googleusercontent.com"

    def authenticate(self, request, token=None):
        matches = []

        try:
            #  Validate the token from Google
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GoogleAuthenticationBackend.CLIENT_ID)
            email = idinfo['email']

            #  If is true, return the currect user
            matches = User.objects(email__iexact=email)
            if len(matches) > 0:
                return matches[0]

            # check emails with case insensitive
            for user in User.objects():
                if str(user.email).lower() == str(email):
                    return user
        except:
            pass

        return None
