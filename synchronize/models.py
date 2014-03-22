from urlparse import urlparse
from django.db.models.base import Model
from django.db.models.fields import CharField, TextField, URLField
from utils import ModelMixins

class ArticleModel(Model, ModelMixins):
    AXEL_URLS = ('onet.pl', )
    SPIEGEL_URLS = ('www.spiegel.de', )

    url = CharField(max_length=255, primary_key=True)
    title = CharField(max_length=255, null=True, blank=True)
    article = TextField(null=True, blank=True)
    image_url = URLField(null=True, blank=True)
    audio_url = URLField(null=True, blank=True)

    @property
    def is_downloaded(self):
        return bool(self.title)

    def download(self):
        url = urlparse(self.url)
        print url.hostname
        if url.hostname in ArticleModel.SPIEGEL_URLS:
            print 'Downloading spiegel'
            self.download_spiegel()
        elif url.hostname in ArticleModel.AXEL_URLS:
            print 'Downloading axel'
            self.download_axel()

    def download_spiegel(self):
        pass

    def download_axel(self):
        pass


