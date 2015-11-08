from django.conf.urls import url, patterns

from landing.views import LandingView

urlpatterns = patterns('landing.views',
    url(r'^$', LandingView.as_view(), name='landing')
)