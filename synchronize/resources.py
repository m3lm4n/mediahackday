from django.db.models.query_utils import Q
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from apn.models import APNTokenModel
from synchronize.models import ArticleModel
from synchronize.serializers import ArticleSerializer


class ArticlesResource(GenericAPIView):
    serializer_class = ArticleSerializer

    def post(self, request):
        ArticleModel.objects.filter(Q(audio_url__isnull=True) | Q(title__isnull=True)).delete()

        serializer = self.get_serializer(data=request.DATA)
        if not serializer.is_valid():
            instance = ArticleModel.objects.get(url=request.DATA['url'])
            return Response(data=self.get_serializer(instance).data, status=HTTP_200_OK)
        serializer.save()
        if not serializer.object.is_downloaded:
            if not serializer.object.download():
                return Response(status=HTTP_404_NOT_FOUND)

        APNTokenModel.send_notification(serializer.data['title'])
        return Response(data=serializer.data, status=HTTP_200_OK)

    def get(self, request):
        articles = ArticleModel.objects.filter(title__isnull=False).order_by('time_added')
        serializer = self.get_serializer(articles, many=True)
        return Response(data={'data': serializer.data}, status=HTTP_200_OK)


