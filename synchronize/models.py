from django.db.models.base import Model
from django.db.models.fields import CharField, TextField, URLField
from utils import ModelMixins

class ArticleModel(Model, ModelMixins):
    url = CharField(max_length=255, primary_key=True)
    title = CharField(max_length=255, null=True, blank=True)
    text = TextField(null=True, blank=True)
    image = URLField(null=True, blank=True)

    def download(self):
        pass

    @property
    def is_downloaded(self):
        return bool(self.title)



