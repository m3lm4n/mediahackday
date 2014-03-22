from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
from utils import ModelMixins


class APNTokenModel(Model, ModelMixins):
    token = CharField(primary_key=True, max_length=255)
