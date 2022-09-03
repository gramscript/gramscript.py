class ApiException(Exception):
    """
    This class represents a base Exception thrown when a call to the Telegram API fails.
    In addition to an informative message, it has a `function_name` and a `result` attribute, which respectively
    contain the name of the failed function and the returned result that made the function to be considered  as
    failed.
    """

    def __init__(self, msg, function_name, result):
        super(ApiException, self).__init__(
            "A request to the Telegram API was unsuccessful. {0}".format(msg))
        self.function_name = function_name
        self.result = result


class ApiHTTPException(ApiException):
    """
    This class represents an Exception thrown when a call to the 
    Telegram API server returns HTTP code that is not 200.
    """

    def __init__(self, function_name, result):
        super(ApiHTTPException, self).__init__(
            "The server returned HTTP {0} {1}. Response body:\n[{2}]"
            .format(result.status_code, result.reason, result.text.encode('utf8')),
            function_name,
            result)


class ApiInvalidJSONException(ApiException):
    """
    This class represents an Exception thrown when a call to the 
    Telegram API server returns invalid json.
    """

    def __init__(self, function_name, result):
        super(ApiInvalidJSONException, self).__init__(
            "The server returned an invalid JSON response. Response body:\n[{0}]"
            .format(result.text.encode('utf8')),
            function_name,
            result)


class ApiTelegramException(ApiException):
    """
    This class represents an Exception thrown when a Telegram API returns error code.
    """

    def __init__(self, function_name, result, result_json):
        super(ApiTelegramException, self).__init__(
            "Error code: {0}. Description: {1}"
            .format(result_json['error_code'], result_json['description']),
            function_name,
            result)
        self.result_json = result_json
        self.error_code = result_json['error_code']
        self.description = result_json['description']
