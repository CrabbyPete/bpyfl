#from django.contrib.auth.decorators import  login_required
from django.conf.urls.defaults      import patterns, url

urlpatterns = patterns('base.views',

    # default index
    url(r'^$',          'home',          name='home'               ),
    url(r'^teams/$',    'teams',         name='teams'              ),
    url(r'^schedule/$', 'schedule',      name='schedule'           ),
    url(r'^standings/$','standings',     name='standings'          ),
    url(r'^officers/$', 'officers',      name='officers'           ),

)

