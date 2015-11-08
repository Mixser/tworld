from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from base.models import User


class SignUpForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password_confirmation = forms.CharField(label='Confirmation', widget=forms.PasswordInput(attrs={'placeholder': 'Confirmation'}))

    class Meta:
        model = User
        fields = ('email', )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_class = 'sign-up'

        self.helper.layout = Layout(
            'email',
            'password',
            'password_confirmation',
            Submit('submit', 'Sign Up')
        )


class SignInForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_class = 'sign-in'

        self.helper.layout = Layout(
            'email',
            'password',
            Submit('submit', 'Sign In')
        )
