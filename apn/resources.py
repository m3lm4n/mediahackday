from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from apn.models import APNTokenModel

__author__ = 'bim'

class TokenResource(GenericAPIView):
    permission_classes = ()
    def post(self, request):
        APNTokenModel.create(token=request.DATA.get('token'))
        return Response(data={'success': True}, status=status.HTTP_200_OK)

class TokenTestResource(GenericAPIView):
    permission_classes = ()
    def get(self, request):
        title = request.GET.get('title', 'Testing...')
        APNTokenModel.send_notification(title)
        return Response(data={'success': True, 'title': title}, status=status.HTTP_200_OK)
