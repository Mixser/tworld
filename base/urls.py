from django.conf.urls import url, patterns

from base.views import DashboardView

urlpatterns = patterns('base.views',
    url(r'^dashboard/?', DashboardView.as_view(), name='dashboard')
)