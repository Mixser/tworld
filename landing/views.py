from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic import View, CreateView

from base.models import User
from landing.forms import SignUpForm, SignInForm


class LandingView(View):
    template_name = 'landing/landing_base.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'landing/sign_in_form.html'
    success_url = reverse_lazy('dashboard')

