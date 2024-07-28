import time
from django.utils.deprecation import MiddlewareMixin
from django.db import connection
from django.conf import settings

class StatsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            total = time.time() - request.start_time
            response['X-Total-Time'] = int(total * 1000)
            response['X-Total-Queries'] = len(connection.queries)
        return response