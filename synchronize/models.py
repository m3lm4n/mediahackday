from urlparse import urlparse
from django.db.models.base import Model
from django.db.models.fields import CharField, TextField, URLField, DateTimeField, BooleanField
from django.utils import timezone
from utils import ModelMixins
import requests
import json
import urllib
import re

class ArticleModel(Model, ModelMixins):
    AXEL_URLS = ('www.welt.de', 'welt.de', 'sportbild.de', 'www.sportbild.de', 'bild.de', 'www.bild.de',
                 'computerbild.de', 'www.computerbild.de', 'rollingstone.de', 'www.rollingstone.de'
    )
    SPIEGEL_URLS = ('www.spiegel.de', )

    url = CharField(max_length=255, primary_key=True)
    title = CharField(max_length=255, null=True, blank=True)
    article = TextField(null=True, blank=True)
    image_url = URLField(null=True, blank=True)
    audio_url = URLField(null=True, blank=True)

    time_added = DateTimeField(blank=True, auto_now_add=True, verbose_name='Created at')

    @property
    def is_downloaded(self):
        return bool(self.title)

    def download(self):
        url = urlparse(self.url)
        print url.hostname
        if url.hostname in ArticleModel.SPIEGEL_URLS:
            print 'Downloading spiegel'
            self.download_spiegel(url)
        elif url.hostname in ArticleModel.AXEL_URLS:
            print 'Downloading axel'
            self.download_axel(url)

    def download_spiegel(self, url):
        pass

    def download_axel(self, url):
        query = self.url
        if url.hostname == 'welt.de' or url.hostname == 'www.welt.de':
            matches = re.search("article([0-9]+?)/", self.url, re.S)
            query =  matches.group(1)

        print 'http://ipool-extern.s.asideas.de:9090/api/v2/search?q=%22http%3A%2F%2Fwww.welt.de%2Fvermischtes%2Farticle126077386%2FChina-meldet-Sichtung-moeglicher-Wrackteile.html%22&limit=1'
        url = 'http://ipool-extern.s.asideas.de:9090/api/v2/search?q=%s&limit=1' % urllib.quote_plus('"%s"' % query)
        print url
        response = requests.get(url)
        try:
            data = json.loads(response.content)
        except ValueError:
            return False
        article = data['documents'][0]
        biggest = {}
        if 'medias' in article:
            for media in  article['medias']:
                if media['type'] == 'PICTURE':
                    max_pow = 0
                    for ref in media['references']:
                        if not 'width' in ref or not 'height' in ref:
                            continue

                        pow = ref['width']*ref['height']
                        if max_pow < pow:
                            max_pow = pow
                            biggest = ref

        if data['documents']:
            self.title = article['title']
            self.article = article['content']
            self.image_url = biggest.get('url')



