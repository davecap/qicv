from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from cv.views import AllCVListView, MyCVListView, CVDetailView, \
                    CVCreateView, CVRequestView, CVEditView

urlpatterns = patterns('',
    url(r'^all/$', login_required(AllCVListView.as_view()), name='all'),
    url(r'^my/$', login_required(MyCVListView.as_view()), name='my'),
    url(r'^create/$', login_required(CVCreateView.as_view()), name='create'),
    url(r'^request/(?P<pk>\d+)/$', login_required(CVRequestView.as_view()), name='request'),
    url(r'^edit/(?P<pk>\d+)/$', login_required(CVEditView.as_view()), name='edit'),
    url(r'^(?P<pk>\d+)/$', login_required(CVDetailView.as_view()), name='cv'),
)
