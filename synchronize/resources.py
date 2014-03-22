from django.http.response import HttpResponseBadRequest
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from synchronize.serializers import ArticleSerializer


class ArticleResource(GenericAPIView):
    serializer_class = ArticleSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        if not serializer.object.is_downloaded:
            serializer.object.download()

        return Response(data=serializer.data, status=HTTP_200_OK)

