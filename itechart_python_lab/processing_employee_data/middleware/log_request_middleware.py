import json
import logging


logging.basicConfig(
    filename='request.log',
    filemode='a',
    format='%(asctime)s %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger('django.request')


class HttpMethods:
    PUT = 'PUT'
    POST = 'POST'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    CONNECT = 'CONNECT'
    OPTIONS = 'OPTIONS'
    TRACE = 'TRACE'
    HEAD = 'HEAD'

    METHODS_WITH_BODY = (PUT, POST, PATCH)


class LogRequestMiddleware:
    """This logger is used to write the request info to the request.log file."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.log_request_info(request)
        response = self.get_response(request)
        return response

    def log_request_info(self, request):
        log_data = {
            'remote_address': request.META['REMOTE_ADDR'],
            'request_method': request.method,
            'request_path': request.get_full_path(),
        }

        if request.method in HttpMethods.METHODS_WITH_BODY:
            log_data['request_body'] = json.loads(str(request.body, 'utf-8'))

        log.info(msg=log_data)
