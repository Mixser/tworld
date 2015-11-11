from django.shortcuts import render
from django.views.generic import View

from wot_api.objects import User
# Create your views here.


class DashboardView(View):
    template_name = 'base/dashboard.html'

    def get(self, request):
        account = request.api.get_by_nickname('mike')
        tanks = account.tanks[0]

        # print tanks.stats

        return render(request, self.template_name, {'account': account, 'tanks': [tanks] })
