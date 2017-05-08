from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer, RefreshJSONWebTokenSerializer,
    VerifyJSONWebTokenSerializer
)


jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class CustomJSONWebTokenAPIView(JSONWebTokenAPIView):

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.object.get('user') or request.user
        token = serializer.object.get('token')
        response_data = jwt_response_payload_handler(token, user, request)

        return Response(response_data)


class ObtainJSONWebToken(CustomJSONWebTokenAPIView):

    serializer_class = JSONWebTokenSerializer


class VerifyJSONWebToken(CustomJSONWebTokenAPIView):

    serializer_class = VerifyJSONWebTokenSerializer


class RefreshJSONWebToken(CustomJSONWebTokenAPIView):

    serializer_class = RefreshJSONWebTokenSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()
refresh_jwt_token = RefreshJSONWebToken.as_view()
verify_jwt_token = VerifyJSONWebToken.as_view()
