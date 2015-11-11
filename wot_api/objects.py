class ApiObject(object):
    def __init__(self, api, data):
        self._data = data
        self.__set_value(None, data)
        self._api = api

    def __set_value(self, key, value):
        if isinstance(value, dict):
            for k, v in value.items():
                self.__set_value(k, v)
        else:
            setattr(self, key, value)

    @classmethod
    def build_from_response(cls, api, data):
        return cls(api, data)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self._data)


class AccountInfo(ApiObject):
    pass


class TankEncyclopediaInfo(ApiObject):
    pass


class TankStats(ApiObject):
    pass


class Tank(ApiObject):
    ENCYCLOPEDIA_INFO = 'encyclopedia/vehicles'
    TANK_STATS = 'tanks/stats'

    def __init__(self, api, data):
        super(Tank, self).__init__(api, data)
        self._encyclopedia_info = None
        self._stats = None

    def __get_encyclopedia_info(self):
        params = {'tank_id': self.tank_id}
        return ObjectIterator(self._api, self.ENCYCLOPEDIA_INFO, TankEncyclopediaInfo, params).get_single_result()

    @property
    def encyclopedia_info(self):
        if not self._encyclopedia_info:
            self._encyclopedia_info = self.__get_encyclopedia_info()
        return self._encyclopedia_info

    @property
    def stats(self):
        print 'try to get stats'
        if not self._stats:
            params = {'account_id': self.account_id}
            self._stats = ObjectIterator(self._api, self.ENCYCLOPEDIA_INFO, TankStats, params).get_first_result()
        return self._stats

    def __str__(self):
        return "%s" % self.tank_id


class User(ApiObject):
    SEARCH_URL = 'account/list'
    PROFILE_INFO = 'account/info'
    TANKS = 'account/tanks'

    def __init__(self, api, data):
        super(User, self).__init__(api, data)
        self._info = None
        self._tanks = None

    @classmethod
    def get_user_by_nickname(cls, api, name):
        """
        :param api:wot_api.api.Api
        :param name: str
        :return: User
        """
        return ObjectIterator(api, cls.SEARCH_URL, User, params={'search': name, 'type': 'exact'}).get_single_result()

    @classmethod
    def search_by_nickname(cls, api, nickname, params=None):
        """
        :param api: wot_api.api.Api
        :param nickname: str
        :param params: dict
        :return: ObjectIterator
        """
        params = params or {}
        params['search'] = nickname
        return ObjectIterator(api, cls.SEARCH_URL, User, params=params)

    def __get_info(self, params=None):
        params = params or {}
        params['account_id'] = self.account_id
        obj_iterator = ObjectIterator(self._api, self.PROFILE_INFO, AccountInfo, params=params)
        return obj_iterator.get_single_result()

    def __get_tanks(self, params=None):
        params = params or {}
        params['account_id'] = self.account_id
        return ObjectIterator(self._api, self.TANKS, Tank, params=params)

    @property
    def info(self):
        if not self._info:
            self._info = self.__get_info()
        return self._info

    @property
    def tanks(self):
        if self._tanks is None:
            tank_list = map(lambda x: setattr(x, 'account_id', self.account_id) or x, self.__get_tanks())
            self._tanks = tank_list
        return self._tanks

    def __str__(self):
        return 'User: %s %s' % (self.account_id, self.nickname)


class ObjectIterator(object):
    def __init__(self, api, source, target_object_class, params=None):
        self._api = api
        self._params = params
        self._target_object_class = target_object_class
        self._queue = []
        self._method = source
        self.load_objects()

    def __iter__(self):
        return self

    def __next__(self):
        if not self._queue:
            raise StopIteration
        return self._queue.pop()

    def get_single_result(self):
        if len(self._queue) == 1:
            return self.next()
        raise ValueError("The API returned multiply objects, but you are expecting only one.")

    def get_first_result(self):
        return self.next()

    next = __next__

    def load_objects(self):
        response = self._api.call(self._method, params=self._params)
        if response.is_success():
            json_response = response.json()
            data = json_response.get('data', [])
            if isinstance(data, dict):
                unpacked_values = []
                for key, value in data.items():
                    if isinstance(value, list):
                        unpacked_values.extend(value)
                    elif isinstance(value, dict):
                        unpacked_values.append(value)
                data = unpacked_values

            result = map(lambda x: self._target_object_class.build_from_response(self._api, x), data)

            self._queue = result
        else:
            raise response.error()
