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
    AXEL_URLS = ('welt.de', 'sportbild.de', 'bild.de', 'computerbild.de', 'rollingstone.de')
    SPIEGEL_URLS = ('spiegel.de', )

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
        return_val = None
        url = urlparse(self.url)
        print url.hostname
        stripped_host = ".".join(url.hostname.rsplit(".")[-2:])
        if stripped_host in ArticleModel.SPIEGEL_URLS:
            print 'Downloading spiegel'
            return_val = self.download_spiegel(stripped_host)
        elif stripped_host in ArticleModel.AXEL_URLS:
            print 'Downloading axel'
            return_val= self.download_axel(stripped_host)

        self.save()
        return return_val

    def download_spiegel(self, url):
        pass

    def download_axel(self, stripped_host):
        query = self.url
        if stripped_host == 'welt.de':
            matches = re.search("article([0-9]+?)/", self.url, re.S)
            query =  matches.group(1)

        if stripped_host == 'bild.de' or stripped_host == 'sportbild.de':
            matches = re.search("([0-9]{6,})", self.url, re.S)
            query =  matches.group(1)

        url = 'http://ipool-extern.s.asideas.de:9090/api/v2/search?q=%s&limit=1' % urllib.quote_plus('"%s"' % query)
        print url
        response = requests.get(url)
        try:
            data = json.loads(response.content)
        except ValueError:
            return False
        if not data['documents']:
            return False
        article = data['documents'][0]
        biggest = {}
        if 'medias' in article:
            for media in  article['medias']:
                if media['type'] == 'PICTURE':
                    max_pow = 0
                    for ref in media['references']:
                        if not 'width' in ref or not 'height' in ref:
                            if not biggest.keys():
                                biggest = ref
                            continue

                        pow = ref['width']*ref['height']
                        if max_pow < pow:
                            max_pow = pow
                            biggest = ref

        if data['documents']:
            self.title = article['title']
            self.article = article['content']
            self.image_url = biggest.get('url')



