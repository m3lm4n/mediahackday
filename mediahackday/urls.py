from django.conf.urls import patterns, include, url
from apn.resources import TokenResource
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()
from synchronize.resources import ArticleResource, ArticlesResource
admin.autodiscover()
from synchronize.resources import ArticleResource

urlpatterns = patterns('',
    # Examples:
    url(r'^token/$', TokenResource.as_view(), name='token'),
    url(r'^synchronize/article/$', ArticleResource.as_view(), name='synchronize'),

    url(r'^articles/$', ArticlesResource.as_view(), name='articles'),
    # url(r'^mediahackday/', include('mediahackday.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^hook/', include('github_hook.urls'))
)
