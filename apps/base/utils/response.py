from rest_framework.response import Response
from rest_framework import status as http_status


class response:
    @staticmethod
    def success(message=None, data=None):
        response_data = { 'error': False }

        if message is not None:
            response_data['message'] = message

        if data is not None:
            response_data['data'] = data

        return Response(response_data, status=http_status.HTTP_200_OK)

    @staticmethod
    def failed(message, status=http_status.HTTP_400_BAD_REQUEST):

        response_data = {
            'error'  : True,
            'message': message
        }

        return Response(response_data, status=status)