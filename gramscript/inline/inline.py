from gramscript.convert import _convert_list_json_serializable
from gramscript.request import _make_request


def answer_inline_query(token, inline_query_id, results, cache_time=None, is_personal=None, next_offset=None,
                        switch_pm_text=None, switch_pm_parameter=None):
    method_url = 'answerInlineQuery'
    payload = {'inline_query_id': inline_query_id,
               'results': _convert_list_json_serializable(results)}
    if cache_time is not None:
        payload['cache_time'] = cache_time
    if is_personal is not None:
        payload['is_personal'] = is_personal
    if next_offset is not None:
        payload['next_offset'] = next_offset
    if switch_pm_text:
        payload['switch_pm_text'] = switch_pm_text
    if switch_pm_parameter:
        payload['switch_pm_parameter'] = switch_pm_parameter
    return _make_request(token, method_url, params=payload, method='post')


def answer_callback_query(token, callback_query_id, text=None, show_alert=None, url=None, cache_time=None):
    """
    Use this method to send answers to callback queries sent from inline keyboards. The answer will be displayed to the user as a notification at the top of the chat screen or as an alert. On success, True is returned.
    Alternatively, the user can be redirected to the specified Game URL. For this option to work, you must first create a game for your bot via BotFather and accept the terms. Otherwise, you may use links like telegram.me/your_bot?start=XXXX that open your bot with a parameter.
    :param token: Bot's token (you don't need to fill this)
    :param callback_query_id: Unique identifier for the query to be answered
    :param text: (Optional) Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters
    :param show_alert: (Optional) If true, an alert will be shown by the client instead of a notification at the top of the chat screen. Defaults to false.
    :param url: (Optional) URL that will be opened by the user's client. If you have created a Game and accepted the conditions via @Botfather, specify the URL that opens your game – note that this will only work if the query comes from a callback_game button.
    Otherwise, you may use links like telegram.me/your_bot?start=XXXX that open your bot with a parameter.
    :param cache_time: (Optional) The maximum amount of time in seconds that the result of the callback query may be cached client-side. Telegram apps will support caching starting in version 3.14. Defaults to 0.
    :return:
    """
    method_url = 'answerCallbackQuery'
    payload = {'callback_query_id': callback_query_id}
    if text:
        payload['text'] = text
    if show_alert is not None:
        payload['show_alert'] = show_alert
    if url:
        payload['url'] = url
    if cache_time is not None:
        payload['cache_time'] = cache_time
    return _make_request(token, method_url, params=payload, method='post')
