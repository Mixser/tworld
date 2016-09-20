from django.conf.urls import url, patterns

from base.views import DashboardView, AccountProfileView, AccountTanksView, TankInfoView, AccountStatisticView

urlpatterns = patterns('base.views',
    url(r'^dashboard/?', DashboardView.as_view(), name='dashboard'),

    # account info
    url(r'^account/(?P<account_id>\d+)/?$', AccountProfileView.as_view(), name='account_profile'),
    url(r'^account/(?P<account_id>\d+)/statistics/?$', AccountStatisticView.as_view(), name='account_statistic'),
    url(r'^account/(?P<account_id>\d+)/tanks/?$', AccountTanksView.as_view(), name='account_tanks'),
    url(r'^account/(?P<account_id>\d+)/tanks/(?P<tank_id>\d+)/?$', TankInfoView.as_view(), name='tank_stats'),


)