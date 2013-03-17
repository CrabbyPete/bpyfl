from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('',
    url(r'^$',          'base.views.home',    name='home' ),
    (r'^base/',         include('base.urls')                      ),
 )


if settings.DEBUG:
    re = r'^media/(?P<path>.*)$'
    urlpatterns += patterns('',
        (re, 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    )

    pass

