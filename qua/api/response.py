from rest_framework.response import Response


def get_response_dict(ok=1, response=None):
    return {
        'ok': ok,
        'response': response
    }


class QuaApiResponse(Response):
    def __init__(self, data=None, status=None, template_name=None,
        headers=None, content_type=None
    ):
        super(QuaApiResponse, self).__init__(
            data=get_response_dict(response=data),
            status=status,
            template_name=template_name, headers=headers,
            content_type=content_type
        )


def custom_jwt_response_payload_handler(token, user=None, request=None):
    return get_response_dict(response={ 'token': token })
