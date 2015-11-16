from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from base.forms import SearchForm


class DashboardView(View):
    template_name = 'base/dashboard.html'

    def get(self, request):
        search_form = SearchForm(request.api, request.GET)
        users = []
        if search_form.is_valid():
            users = search_form.search()
        return render(request, self.template_name, {'search_form': search_form, 'users': users})


class AccountProfileView(View):
    template_name = 'base/account_profile.html'

    def get(self, request, account_id):
        account_info = request.api.get_user_info_by_account_id(int(account_id))
        return render(request, self.template_name, {'account_id': account_id, 'account_info': account_info})


class AccountTanksView(View):
    template_name = 'base/account_tanks.html'

    def get(self, request, account_id):
        tanks = request.api.get_account_tanks(account_id)
        return render(request, self.template_name, {'tanks': tanks})


class TankInfoView(View):
    template_name = 'base/tank_stats.html'

    def get(self, request, account_id, tank_id):
        tank_stats = request.api.get_tank_info(account_id, tank_id)
        return render(request, self.template_name, {'tank_stats': tank_stats})


