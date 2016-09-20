from django.conf import settings
from django.core.urlresolvers import resolve
from wot_api.api import Api


class CreateApiObjectMiddleware(object):
    def process_request(self, request):
        # if request.user.is_authenticated():
        request.api = Api(settings.WOT_API_ID)
        request.url_name = resolve(request.path).url_name

    def process_view(self, request, view_func, view_args, view_kwargs):
        """

        :param request:
        :param view_func:
        :param view_args:
        :param view_kwargs:
        :return:
        """
        if 'account_id' in view_kwargs:
            request.account_id = view_kwargs.get('account_id')

