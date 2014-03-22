from rest_framework.generics import GenericAPIView

__author__ = 'bim'

class TokenResource(GenericAPIView):
    permission_classes = ()
    def post(self, request):
        print request.DATA.get('token')
