from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web_framework.server_side.infastructure.auth.talpiot_jwt_authentication import TalpiotJWTAuthentication


class UserGetView(APIView):
    authentication_classes = [TalpiotJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'user': {
            'name': request.user.name,
            'email': request.user.email,
            'mahzor': request.user.mahzor
        }})
