from django.http.response import HttpResponseBadRequest
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from synchronize.models import ArticleModel
from synchronize.serializers import ArticleSerializer


class ArticlesResource(GenericAPIView):
    serializer_class = ArticleSerializer
    def post(self, request):
        ArticleModel.objects.filter(title__isnull=True).delete()

        serializer = self.get_serializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        if not serializer.object.is_downloaded:
            if not serializer.object.download():
                return Response(status=HTTP_404_NOT_FOUND)

        return Response(data=serializer.data, status=HTTP_200_OK)

    def get(self, request):
        articles = ArticleModel.objects.order_by('time_added')
        serializer = self.get_serializer(articles, many=True)
        return Response(data={'data': serializer.data}, status=HTTP_200_OK)