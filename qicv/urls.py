from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.http import HttpResponseServerError
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
from django.template import Context, loader

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'index.html'}, name='index'),
    # url(r'^qicv/', include('qicv.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# urlpatterns += patterns('',
#     url(r'^APP/', include('apps.APP.urls', namespace='APP', app_name='APP')),
# )

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('django.views.static',
        url(r'^media/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )


def handler500(request):
    t = loader.get_template('500.html')
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))
