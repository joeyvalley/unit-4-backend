import logging


class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only log errors
        if response.status_code >= 400:
            logger = logging.getLogger(__name__)
            logger.error(
                f"{request.method} {request.path} "
                f"returned {response.status_code} {response.reason_phrase}"
            )

        return response
