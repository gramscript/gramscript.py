from ..api import ApiHTTPException, ApiInvalidJSONException, ApiTelegramException


def _check_result(method_name, result):
    """
    Checks whether `result` is a valid API response.
    A result is considered invalid if:
        - The server returned an HTTP response code other than 200
        - The content of the result is invalid JSON.
        - The method call was unsuccessful (The JSON 'ok' field equals False)

    :raises ApiException: if one of the above listed cases is applicable
    :param method_name: The name of the method called
    :param result: The returned result of the method request
    :return: The result parsed to a JSON dictionary.
    """
    try:
        result_json = result.json()
    except:
        if result.status_code != 200:
            raise ApiHTTPException(method_name, result)
        else:
            raise ApiInvalidJSONException(method_name, result)
    else:
        if not result_json['ok']:
            raise ApiTelegramException(method_name, result, result_json)

        return result_json
