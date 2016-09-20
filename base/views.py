from datetime import timedelta
from django.core.urlresolvers import reverse
from django.db.models import Avg, Max, Func
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from django.views.generic import View
from base.forms import SearchForm, AddAccountForm
from base.models import AccountStatistic, WotAccount, TankStatistic, Tank


class DashboardView(View):
    template_name = 'base/dashboard.html'

    def get(self, request):
        search_form = SearchForm(request.api, request.GET)
        users = []
        if search_form.is_valid():
            users = search_form.search()
        accounts = WotAccount.objects.all()[:10]
        context = {'search_form': search_form,
                   'users': users,
                   'accounts': accounts
                   }
        return render(request, self.template_name, context)


class AccountProfileView(View):
    template_name = 'base/account_profile.html'

    def get(self, request, account_id):
        need_actual_data = request.GET.get('force', False)
        form = None
        if WotAccount.objects.filter(account_id=account_id).exists() and not need_actual_data:
            account = WotAccount.objects.prefetch_related('statistics').get(account_id=account_id)
            account_statistics = account.statistics.last()
            if not account_statistics:
                account_info = request.api.get_user_info_by_account_id(int(account_id))
                account_statistics = AccountStatistic.objects.build_from_api_object(account_info)
        elif not need_actual_data:
            account_info = request.api.get_user_info_by_account_id(int(account_id))
            form = AddAccountForm(account_info)
            account_statistics = AccountStatistic.objects.build_from_api_object(account_info, False)
        else:
            account_info = request.api.get_user_info_by_account_id(int(account_id))
            account_statistics = AccountStatistic.objects.build_from_api_object(account_info)
        context = {
            'form': form,
            'account_statistics': account_statistics
        }

        return render(request, self.template_name, context)

    def post(self, request, account_id):
        form = AddAccountForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('account_profile', args={'account_id': user.account_id}))


class AccountTanksView(View):
    template_name = 'base/account_tanks.html'

    def get(self, request, account_id):
        api_tanks = list(request.api.get_account_tanks(account_id))
        tank_ids = set(map(lambda x: x.tank_id, api_tanks))

        existing_tanks = set(Tank.objects.values_list('tank_id', flat=True))

        tank_ids = tank_ids - existing_tanks

        tanks = map(lambda x: Tank(tank_id=x), tank_ids)

        Tank.objects.bulk_create(tanks)

        tanks = Tank.objects.filter(tank_id__in=tank_ids)
        account = WotAccount.objects.get(account_id=account_id)
        tank2account_relations = [Tank.accounts.through(tank=tank, wotaccount=account) for tank in tanks]
        Tank.accounts.through.objects.bulk_create(tank2account_relations)

        return render(request, self.template_name, {'tanks': api_tanks})


class TankInfoView(View):
    template_name = 'base/tank_stats.html'

    def get(self, request, account_id, tank_id):
        refresh_timedelta = datetime.now() - timedelta(minutes=5)
        query_params = dict(account_id=account_id, tank_id=tank_id, created_at__gt=refresh_timedelta)
        obj_created_less_than_5_minutes = TankStatistic.objects.filter(**query_params)

        if False:
            api_tank_stats = request.api.get_tank_info(account_id, tank_id)
            tank_stats = TankStatistic.objects.build_from_api_object(api_tank_stats)
        else:
            tank_stats = obj_created_less_than_5_minutes.first()
        return render(request, self.template_name, {'tank_stats': tank_stats})


class AccountStatisticView(View):
    template_name = 'base/account_statistics.html'

    def get(self, request, account_id):
        fields = request.GET.getlist('fields', ['wins', 'losses'])
        account_statistics = AccountStatistic.objects.filter(account_id=account_id)
        dates = map(lambda x: "{0.month}/{0.day}/{0.year} {0.hour}:{0.minute}".format(x.created_at), account_statistics)
        data = []
        for field in fields:
            field_data = map(lambda x: getattr(x, field), account_statistics)
            data.append(field_data)

        data.sort(reverse=True)
        context = {
            'dates': dates,
            'data': data
        }
        return render(request, self.template_name, context)
