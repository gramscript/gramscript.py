from gramscript.request import _make_request


def get_chat(token, chat_id):
    method_url = r'getChat'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload)


def leave_chat(token, chat_id):
    method_url = r'leaveChat'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload)


def get_chat_administrators(token, chat_id):
    method_url = r'getChatAdministrators'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload)


def get_chat_member_count(token, chat_id):
    method_url = r'getChatMemberCount'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload)


def set_sticker_set_thumb(token, name, user_id, thumb):
    method_url = r'setStickerSetThumb'
    payload = {'name': name, 'user_id': user_id}
    files = {}
    if thumb:
        if not isinstance(thumb, str):
            files['thumb'] = thumb
        else:
            payload['thumb'] = thumb
    return _make_request(token, method_url, params=payload, files=files or None)


def set_chat_sticker_set(token, chat_id, sticker_set_name):
    method_url = r'setChatStickerSet'
    payload = {'chat_id': chat_id, 'sticker_set_name': sticker_set_name}
    return _make_request(token, method_url, params=payload)


def delete_chat_sticker_set(token, chat_id):
    method_url = r'deleteChatStickerSet'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload)


def get_chat_member(token, chat_id, user_id):
    method_url = r'getChatMember'
    payload = {'chat_id': chat_id, 'user_id': user_id}
    return _make_request(token, method_url, params=payload)
