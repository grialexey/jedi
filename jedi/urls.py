from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
#    (r'^$', "ads.views.listing_of_ads"),
    (r'^jediadmin/', include(admin.site.urls)),
#    (r'^getjson/$', "ads.views.json_query"),
    (r'^$', "ads.views.listing_of_ads"),
    (r'^(?P<query>[^/]+)$', "ads.views.listing_of_ads"),
#    (r'', include('jedi.base.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL[1:-1],
                'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
            (r'^404/$', 'django.views.defaults.page_not_found'),
            (r'^500/$', 'django.views.defaults.server_error'),
            (r'^admin/', include(admin.site.urls)),
    )