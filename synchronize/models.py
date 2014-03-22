import urllib
from urlparse import urlparse
from django.db.models.base import Model
from django.db.models.fields import CharField, TextField, URLField, DateTimeField, BooleanField
from django.utils import timezone
from utils import ModelMixins
from xml.dom import minidom
import requests
import json
import re
import hashlib

class ArticleModel(Model, ModelMixins):
    AXEL_URLS = ('welt.de', 'sportbild.de', 'bild.de', 'computerbild.de', 'abendblatt.de', 'morgenpost.de')
    SPIEGEL_URLS = ('spiegel.de', )

    API_KEY = "XhnrxYi7fiGrU4kFWxMVmUKHmIz19d7e"

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
        query = self.url
        matches = re.search("[^0-9]([0-9]+)\.html", self.url, re.S)
        query = matches.group(1)

        print 'http://dis.spiegel.de/sp-services/vdz/search/%s?user=Hackday:20142014' % query

        url = 'http://dis.spiegel.de/sp-services/vdz/search/%s?user=Hackday:20142014' % query
        response = requests.get(url)
        try:
            dom = minidom.parseString(response.content)
        except:
            return False

        title = dom.getElementsByTagName('titel')[0].childNodes[0].nodeValue

        art_id = dom.getElementsByTagName('dokument')[0].getAttribute('id')

        url = 'http://dis.spiegel.de/sp-services/vdz/document/%s?user=Hackday:20142014' % art_id
        response = requests.get(url)

        try:
            dom = minidom.parseString(response.content)
        except:
            return False

        matches = re.search("artikel>(.*?)<\/artikel>", response.content, re.S)
        article = matches.group(1)
        article = re.sub("<(.*?)>"," ",article)

        self.article = article

        self.generate_sound_file(article)

        return True

    def download_axel(self, stripped_host):
        query = self.url
        if stripped_host == 'welt.de' or stripped_host == 'abendblatt.de' or stripped_host == 'morgenpost.de':
            matches = re.search("article([0-9]+?)/", self.url, re.S)
        if stripped_host == 'computerbild.de':
            matches = re.search("([0-9]+?)\.html", self.url, re.S)
        if stripped_host == 'bild.de' or stripped_host == 'sportbild.de':
            matches = re.search("([0-9]{6,})", self.url, re.S)

        if not matches:
            return False
        query =  matches.group(1)
        url = 'http://ipool-extern.s.asideas.de:9090/api/v2/search?q=%s&limit=1' % urllib.quote_plus('"%s"' % query)
        print url
        response = requests.get(url)
        try:
            data = json.loads(response.content)
        except ValueError:
            return False

        print data
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
            self.generate_sound_file(self.article)

        return True

    def md5(self, str):
        return hashlib.md5(str).hexdigest()

    def generate_sound_file(self, text):
        text = re.sub(r'<[^>]*?>', '', text)[:200]
        api_url = 'http://api.ivona.com/api/saas/rest/'

        response = requests.post(api_url + 'tokens/', params = { "email": "a.lastowski@nomtek.com"})

        token = response.content[1:-1]

        params = {
            "token": token,
            "md5" : self.md5( self.md5(self.API_KEY) + token),
            "text": text,
            "contentType": "text/plain",
            "voiceId": "de_hans",
            "codecId": "mp3/22050"
        }
        print params
        response = requests.post(api_url + 'speechfiles/', params = params)
        try:
            data = json.loads(response.content)
        except ValueError:
            print response.content
            return False

        print data
        if "soundUrl" in data:
            self.audio_url = data["soundUrl"]

        return True


