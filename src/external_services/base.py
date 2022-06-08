import time
from requests import Response


class NotFound(Exception):
    pass


class RateLimit(Exception):
    pass


class BadRequest(Exception):
    pass


class BaseClient():
    def __init__(self):
        self.max_retry = 5

    def response_handler(
        self, request_func, request_params, retry: int = 0,
    ) -> Response:
        response = request_func(**request_params)
        if response.status_code == 400:
            raise BadRequest(response.json())

        if response.status_code == 404:
            raise NotFound

        if response.status_code == 429:
            if retry <= self.max_retry:
                retry += 1
                print(f'{retry} Retrying....')
                time.sleep(5)
                return self._response_handler(
                    request_func, request_params, retry)
            else:
                raise RateLimit

        if response.status_code != 200:
            print(response.status_code)
            print(response.content)
            raise

        return response
