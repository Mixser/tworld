from crispy_forms.bootstrap import StrictButton
from crispy_forms.layout import Layout, Hidden, Submit
from crispy_forms.helper import FormHelper

from django import forms

from base.models import WotAccount


class AddAccountForm(forms.ModelForm):
    account_id = forms.CharField(widget=forms.HiddenInput())
    nickname = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = WotAccount
        fields = ('account_id', 'nickname')


    def __init__(self, *args, **kwargs):
        super(AddAccountForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(
            'nickname',
            'account_id',
            Submit('Add to DB', 'Add to DB')
        )


class SearchForm(forms.Form):
    q = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search by nickname'}))

    def __init__(self,api, *args, **kwargs):
        """
        :type api:wot_api.api.Api
        """
        super(SearchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'

        self.api = api

        self.helper.layout = Layout(
            'q',
            StrictButton('Search', type='submit', css_class='btn-default')
        )

    def search(self):
        """
        :rtype:wot_api.objects.ObjectIterator
        """
        q = self.cleaned_data.get('q')
        users = self.api.search_user_by_nickname(q)
        return users
