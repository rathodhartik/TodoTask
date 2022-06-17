from copy import error
from rest_framework import status
from rest_framework.status import *
from rest_framework.response import Response

OK = status.HTTP_200_OK
CREATED = status.HTTP_201_CREATED
BAD_REQUEST =status.HTTP_400_BAD_REQUEST
NO_CONTENT =status.HTTP_204_NO_CONTENT
NOT_FOUND=status.HTTP_404_NOT_FOUND

def success_added(message,data):
    msg={"code":CREATED,
        "message":message,
        "data":data}
    return msg

def data_fail(message,data):
    msg={"code":BAD_REQUEST,
         "message":message,
         "data":data}
    return msg

def success_deleted(message,data):
    msg={"code":OK,
        "message":message,
        "data":data}
    return msg

# class APISuccess:
#     def __new__(cls, status=HTTP_200_OK, message = 'Success', data={}):
#         return Response(
#             {
#                 'status': status,
#                 'message': message,
#                 'data': data
#             },
#             status
#         )

# class APIFailure:
#     def __new__(cls, message = 'Error', status=HTTP_400_BAD_REQUEST):
#         return Response(
#             {
#                 'status': status,
#                 'message': message
#             },
#             status
#         )

