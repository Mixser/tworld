from crispy_forms.bootstrap import StrictButton
from crispy_forms.layout import Layout
from crispy_forms.helper import FormHelper

from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search by nickname'}))

    def __init__(self,api, *args, **kwargs):
        """
        :param api:wot_api.api.Api
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

        :return:wot_api.objects.ObjectIterator
        """
        q = self.cleaned_data.get('q')
        users = self.api.search_user_by_nickname(q)
        return users
