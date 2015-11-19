import requests
import urllib
import json

from wot_api.exceptions import get_exception
from wot_api.objects import User, Tank


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
        """
        :rtype: bool
        """
        json_body = self.json()

        if isinstance(json_body, dict) and json_body.get('status', None) == 'ok':
            return True

        return False

    def is_failure(self):
        return not self.is_success()

    def error(self):
        """
        :rtype: wot_api.exceptions.BaseApiException
        """
        return get_exception(self.json())


class Api(object):
    HOST = 'http://api.worldoftanks.ru/wot/'

    def __init__(self, application_id, language='en'):
        self._application_id = application_id
        self._language = language

    def call(self, path, params=None, headers=None):
        print 'Do call! (%s %s %s)' % (path, params, headers)
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

    def get_account_tanks(self, account_id):
        """
        :type account_id:int
        :rtype: wot_api.objects.ObjectIterator
        """
        return Tank.get_account_tanks(self, account_id)

    def get_by_nickname(self, nickname):
        """
        :type nickname:str
        :rtype: objects.User
        """
        return User.get_user_by_nickname(self, nickname)

    def search_user_by_nickname(self, nickname):
        """
        :type nickname:str
        :rtype: wot_api.objects.ObjectIterator
        """
        return User.search_by_nickname(self, nickname)

    def get_user_info_by_account_id(self, account_id):
        """
        :param account_id: int
        :rtype: wot_api.objects.AccountInfo
        """
        return User.get_user_info_by_account_id(self, account_id)

    def get_tank_info(self, account_id, tank_id):
        """
        :type account_id: int
        :type tank_id: int
        :rtype: wot_api.objects.TankStats
        """
        return Tank.get_account_tanks(self, account_id, tank_id).get_single_result()

if __name__ == "__main__":
    from objects import User

    api = Api(application_id="95b1b0a4aee9778b825653431af5379e")

    tanks = api.get_tank_info(356, 15649)
    print tanks
