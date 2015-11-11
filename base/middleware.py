from django.conf import settings

from wot_api.api import Api


class CreateApiObjectMiddleware(object):
    def process_request(self, request):
        # if request.user.is_authenticated():
        request.api = Api(settings.WOT_API_ID)
