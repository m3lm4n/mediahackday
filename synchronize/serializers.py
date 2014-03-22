from rest_framework.serializers import ModelSerializer
from synchronize.models import ArticleModel


class ArticleSerializer(ModelSerializer):
    class Meta():
        model = ArticleModel
        required_fields = ('url', )
        exclude = ('time_added', )