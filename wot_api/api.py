import requests
import urllib
import json

from wot_api.exceptions import get_exception
from wot_api.objects import User


class ApiResponse(object):
    def __init__(self, body=None, http_status=None, headers=None, call=None):
        self._body = body
        self._http_status = http_status
        self._headers = headers or {}
        self._call = call

    def body(self):
        return self._body

    def __str__(self):
        return self._body

    def json(self):
        try:
            return json.loads(self._body)
        except (TypeError, ValueError):
            return self._body

    def status(self):
        return self._http_status

    def is_success(self):
        json_body = self.json()

        if isinstance(json_body, dict) and json_body.get('status', None) == 'ok':
            return True

        return False

    def is_failure(self):
        return not self.is_success()

    def error(self):
        return get_exception(self.json())


class Api(object):
    HOST = 'http://api.worldoftanks.ru/wot/'

    def __init__(self, application_id, language='en'):
        self._application_id = application_id
        self._language = language

    def call(self, path, params=None, headers=None):
        params = params or {}
        headers = headers or {}

        params['application_id'] = self._application_id
        params['language'] = params.get('language', self._language)

        url = "%s%s/?%s" % (self.HOST, path, urllib.urlencode(params))
        response = requests.request('GET', url=url, headers=headers)

        api_response = ApiResponse(body=response.text, http_status=response.status_code, headers=response.headers)

        if api_response.is_failure():
            raise api_response.error()

        return api_response

    def get_by_nickname(self, nickname):
        """
        :param nickname:str
        :return: objects.User
        """
        return User.get_user_by_nickname(self, nickname)

    def search_user_by_nickname(self, nickname):
        """
        :param nickname:str
        :return: wot_api.objects.ObjectIterator
        """
        return User.search_by_nickname(self, nickname)


if __name__ == "__main__":
    from objects import User

    api = Api(application_id="95b1b0a4aee9778b825653431af5379e")
    user = User.get_user_by_nickname(api, 'mike')
    tank = user.tanks[0]
    print tank.encyclopedia_info
