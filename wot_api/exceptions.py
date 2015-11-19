class BaseApiException(Exception):
    error_description = ""

    def __init__(self, code, message, error_description):
        self.code = code
        message = "%s - %s" % (message, error_description)
        super(BaseApiException, self).__init__(message)


class FieldNotSpecified(BaseApiException):
    error_message = "{}_NOT_SPECIFIED"
    error_description = "Required field {} is not specified."
    code = 402
    pass


class FieldNotFound(BaseApiException):
    error_message = "{}_NOT_FOUND"
    error_description = "Data not found."
    code = 404
    pass


class MethodNotFound(BaseApiException):
    error_message = "METHOD_NOT_FOUND"
    error_description = "Invalid API method."
    code = 404
    pass


class MethodDisabled(BaseApiException):
    error_message = "METHOD_DISABLED"
    error_description = "Specified method is disabled."
    code = 405
    pass


class ListLimitExceeded(BaseApiException):
    error_message = "{}_LIST_LIMIT_EXCEEDED"
    error_description = "Limit of passed-in identifiers in the {} exceeded."
    code = 407
    pass


class ApplicationIsBlocked(BaseApiException):
    error_message = "APPLICATION_IS_BLOCKED"
    error_description = "Application is blocked by the administration."
    code = 407
    pass


class InvalidField(BaseApiException):
    error_message = "INVALID_{}"
    error_description = "Specified field value {} is not valid."
    code = 407
    pass


class InvalidApplicationId(BaseApiException):
    error_message = "INVALID_APPLICATION_ID"
    error_description = "Invalid application_id."
    code = 407
    pass


class InvalidIpAddress(BaseApiException):
    error_message = "INVALID_IP_ADDRESS"
    error_description = "Invalid IP-address for the server application."
    code = 407
    pass


class RequestLimitExceeded(BaseApiException):
    error_message = "REQUEST_LIMIT_EXCEEDED"
    error_description = "Request limit is exceeded."
    code = 407
    pass


class SourceNotAvailable(BaseApiException):
    error_message = "SOURCE_NOT_AVAILABLE"
    error_description = "Data source is not available."
    code = 504
    pass


def get_exception(response_body):
    """
    :type response_body: dict
    :rtype: BaseApiException
    """
    __EXCEPTIONS__ = [FieldNotSpecified, FieldNotFound, MethodNotFound, MethodDisabled, ListLimitExceeded,
                      ApplicationIsBlocked, InvalidField, InvalidApplicationId, InvalidIpAddress, RequestLimitExceeded,
                      SourceNotAvailable]

    error = response_body.get('error')
    code = int(error.get('code'))
    message = error.get('message')
    field = error.get('field', '').upper()

    exceptions = filter(lambda x: x.code == code and x.error_message.format(field) == message, __EXCEPTIONS__)

    if len(exceptions) == 1:
        error_description = exceptions[0].error_description.format(field)
        return exceptions[0](code, message, error_description)
    elif InvalidApplicationId in exceptions:
        return InvalidApplicationId(code, message, InvalidApplicationId.error_description)

    return BaseApiException(code, message, '')
