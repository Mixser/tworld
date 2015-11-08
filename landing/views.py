from django.shortcuts import render
from django.views.generic import View


class LandingView(View):
    template_name = 'landing/landing_base.html'

    def get(self, request):
        return render(request, self.template_name)
