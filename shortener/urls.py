from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('shortener.views',
    url(r'^$', 'index', name='index'),
    url(r'^info/(?P<base62_id>\w+)$', 'info', name='info'),
    url(r'^submit/$', 'submit', name='submit'),
    url(r'^addtag/$', 'addtag', name='addtag'),
    url(r'^(?P<base62_id>\w+)$', 'follow', name='follow'),
)
