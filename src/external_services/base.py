import time
from requests import Response


class NotFound(Exception):
    pass


class RateLimit(Exception):
    pass


class BadRequest(Exception):
    pass


class InternalServerError(Exception):
    pass


class BaseClient():
    def __init__(self):
        self._max_retry = 5
        self._sleep_time_sec = 5

    def response_handler(
        self, request_func, request_params, retry: int = 0,
    ) -> Response:
        try:
            response = request_func(**request_params)
        except Exception as e:
            if retry <= self._max_retry:
                return self._retry_request(request_func, request_params, retry)
            else:
                raise e

        if response.status_code == 500:
            raise InternalServerError

        if response.status_code == 400:
            raise BadRequest(response.json())

        if response.status_code == 404:
            raise NotFound

        if response.status_code == 429:
            if retry <= self._max_retry:
                return self._retry_request(request_func, request_params, retry)
            else:
                raise RateLimit

        if response.status_code != 200:
            print(response.status_code)
            print(response.content)
            raise

        return response

    def _retry_request(self, request_func, request_params, retry: int = 0):
        retry += 1
        print(f'{retry} Retrying....')
        time.sleep(self._sleep_time_sec)
        return self.response_handler(request_func, request_params, retry)
