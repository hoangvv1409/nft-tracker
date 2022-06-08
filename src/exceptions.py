class AppException(Exception):
    _message = 'Internal error'
    http_code = 400
    error_code = 'internal_error'

    def __init__(
        self, code: int = None, error_details: any = None, **params,
    ):
        self.code = code
        self._params = params
        self.error_details = error_details

    @property
    def message(self):
        return self._message.format(**self._params)

    def __str__(self):
        return self.message

    def to_json(self):
        res = {
            'data': self.message,  # deprecated soon
            'error_code': self.error_code,
            'error_message': self.message,
        }

        if self.error_details is not None:
            res['error_details'] = self.error_details

        if self.code is not None:
            res["code"] = self.code

        return res
