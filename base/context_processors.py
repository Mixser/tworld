from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import resolve


def url_names(request):
    """
    :type request: django.core.handlers.wsgi.WSGIRequest
    :rtype: dict
    """
    url_name = resolve(request.path).url_name

    return {'url_name': url_name}
