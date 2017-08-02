import time
import logging


class LoggingMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response
        self.logger = logging.getLogger('qua.requests')

    def process_request(self, request):

        request.timer = time.time()
        request.logger = self.logger

    def process_response(self, request, response):

        self.logger.info(
            '%s [%s] %s (%.3f)',
            request.method,
            response.status_code,
            request.get_full_path(),
            time.time() - request.timer
        )

        return response

    def __call__(self, request):

        self.process_request(request)

        response = self.get_response(request)

        self.process_response(request, response)

        return response
