
class ModelMixins(object):
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.save()
        return instance

    @classmethod
    def read(cls, pk):
        try:
            return cls.objects.get(id=pk)
        except cls.DoesNotExist:
            return None

    @classmethod
    def read_all(cls):
        try:
            return cls.objects.all()
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_model_and_app_name(cls):
        return '%s.%s' % (cls._meta.app_label, cls._meta.object_name)
