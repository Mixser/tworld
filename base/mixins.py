from collections import OrderedDict


class FieldsMixin(object):

    def fields(self):
        """
        :rtype: dict
        """
        result = OrderedDict()
        field_names = self.get_field_names()
        for field_name in field_names:
            result[field_name] = getattr(self, field_name)
        return result

    @classmethod
    def get_field_names(cls):
        """
        :rtype: list
        """
        excluded_fields = getattr(cls, 'excluded_fields', [])
        additional_fields = getattr(cls, 'additional_fields', [])
        field_names = filter(lambda x: x not in excluded_fields, cls._meta.get_all_field_names())
        field_names += additional_fields
        field_names.sort()
        return field_names

