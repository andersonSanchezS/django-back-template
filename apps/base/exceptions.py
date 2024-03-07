from rest_framework.views import exception_handler
from rest_framework.response import Response
import ast

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        if isinstance(exc, HTTPException):
            return Response({'message': exc.message}, status=exc.status_code)

        return Response({'message': exc.message}, status=500)

    return response


class HTTPException(Exception):

    def __init__(self, message, status_code):
        try:
            parsedMessage    = ast.literal_eval(message)
            # if the message isn't a tuple sent a 500 status code
            if not isinstance(parsedMessage, tuple):
                self.message     = parsedMessage
                self.status_code = 500
            else:
                self.message     = parsedMessage[0]
                self.status_code = parsedMessage[1]
            
        except :
            self.message     = message
            self.status_code = status_code