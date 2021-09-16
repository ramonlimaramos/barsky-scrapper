import requests

from barsky_scrapper.errors import (NotFound, InvalidRequest, Accepted,
                        NotAuthorized, Forbidden, ServiceInternalError, Processing)

__all__ = ['HttpMixin']


class HttpMixin:
    headers = {}

    def __init__(self, headers=None):
        if not headers:
            headers = {}
        self.headers = {**self.headers, **headers}

    def get(self, url):
        response = requests.get(url, headers=self.headers)

        status_dict = {
            202: Accepted,
            304: Processing,
            400: InvalidRequest,
            401: NotAuthorized,
            404: NotFound,
            403: Forbidden,
        }

        if response.status_code in status_dict.keys():
            raise status_dict[response.status_code]()

        elif 400 <= response.status_code < 500:
            raise InvalidRequest()

        elif response.status_code >= 500:
            raise ServiceInternalError()

        return response

    def post(self, url):
        pass
