from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from dashboard.views import DashboardView

urlpatterns = patterns('',
    url(r'^$', login_required(DashboardView.as_view()), name='main'),
)
