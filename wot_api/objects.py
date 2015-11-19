from collections import OrderedDict


class FieldsMixin(object):
    def __init__(self, *args, **kwargs):
        super(FieldsMixin, self).__init__(*args, **kwargs)
        self._fields = None

    def fields(self):
        """
        :rtype: OrderedDict
        """
        if not self._fields:
            keys = sorted(filter(lambda x: not x.startswith('_'), self.__dict__.keys()))
            self._fields = OrderedDict()
            for key in keys:
                self._fields[key] = self.__dict__[key]
        return self._fields

    def get(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        return default


class ApiObject(object):
    def __init__(self, api, data):
        self._data = data
        self._namespaces = []
        self.__set_value(None, data)
        self._api = api

    def __set_value(self, key, value, prefix=''):
        if isinstance(value, dict):
            prefix = prefix + '__' + str(key) if prefix else key
            for k, v in value.items():
                self.__set_value(k, v, prefix)
        else:
            if prefix and prefix not in self._namespaces:
                self._namespaces.append(prefix)
            key = prefix + '__' + key if prefix else key
            setattr(self, key, value)

    @classmethod
    def build_from_response(cls, api, data):
        return cls(api, data)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self._data)


class AccountInfo(FieldsMixin, ApiObject):
    pass


class TankEncyclopediaInfo(FieldsMixin, ApiObject):
    pass


class TankStats(FieldsMixin, ApiObject):
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
            self._stats = ObjectIterator(self._api, self.TANK_STATS, TankStats, params).get_first_result()
        return self._stats

    @classmethod
    def get_account_tanks(cls, api, account_id, tank_id=None):
        """
        :rtype: ObjectIterator
        """
        params = {'account_id': account_id, 'tank_id': tank_id or ''}
        return ObjectIterator(api, cls.TANK_STATS, TankStats, params=params)

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
        :type api:wot_api.api.Api
        :type name: str
        :rtype: User
        """
        return ObjectIterator(api, cls.SEARCH_URL, User, params={'search': name, 'type': 'exact'}).get_single_result()

    @classmethod
    def get_user_info_by_account_id(cls, api, account_id, fields=None):
        """

        :type api: wot_api.api.Api
        :type account_id: int
        :type fields: list
        :rtype: AccountInfo
        """
        fields = fields or []
        fields = ','.join(map(lambda x: str(x), fields))
        params = {'account_id': account_id, 'fields': fields}
        account_info = ObjectIterator(api, cls.PROFILE_INFO, AccountInfo, params=params).get_single_result()
        return account_info

    @classmethod
    def search_by_nickname(cls, api, nickname, params=None):
        """
        :type api: wot_api.api.Api
        :type nickname: str
        :type params: dict
        :rtype: ObjectIterator
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
        self.__load_objects()

    def __iter__(self):
        return self

    def __next__(self):
        if not self._queue:
            raise StopIteration
        return self._queue.pop()

    def get_single_result(self):
        if len(self._queue) == 0:
            return None
        if len(self._queue) == 1:
            return self.next()
        raise ValueError("The API returned multiply objects, but you are expecting only one.")

    def get_first_result(self):
        return self.next()

    next = __next__

    def __load_objects(self):
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
