try:
    import ujson as json
except ImportError:
    import json
from datetime import datetime

from gramscript.convert import _convert_list_json_serializable
from gramscript.request import _make_request
from gramscript.util import is_pil_image, is_string, pil_image_to_file


def get_method_by_type(data_type):
    if data_type == 'document':
        return r'sendDocument'
    if data_type == 'sticker':
        return r'sendSticker'


def ban_chat_member(token, chat_id, user_id, until_date=None, revoke_messages=None):
    method_url = 'banChatMember'
    payload = {'chat_id': chat_id, 'user_id': user_id, 'until_date': until_date.timestamp(
    ) if isinstance(until_date, datetime) else until_date}

    if revoke_messages is not None:
        payload['revoke_messages'] = revoke_messages
    return _make_request(token, method_url, params=payload, method='post')


def unban_chat_member(token, chat_id, user_id, only_if_banned):
    method_url = 'unbanChatMember'
    payload = {'chat_id': chat_id, 'user_id': user_id}
    if only_if_banned is not None:  # None / True / False
        payload['only_if_banned'] = only_if_banned
    return _make_request(token, method_url, params=payload, method='post')


def restrict_chat_member(
        token, chat_id, user_id, until_date=None,
        can_send_messages=None, can_send_media_messages=None,
        can_send_polls=None, can_send_other_messages=None,
        can_add_web_page_previews=None, can_change_info=None,
        can_invite_users=None, can_pin_messages=None):
    method_url = 'restrictChatMember'
    permissions = {}
    if can_send_messages is not None:
        permissions['can_send_messages'] = can_send_messages
    if can_send_media_messages is not None:
        permissions['can_send_media_messages'] = can_send_media_messages
    if can_send_polls is not None:
        permissions['can_send_polls'] = can_send_polls
    if can_send_other_messages is not None:
        permissions['can_send_other_messages'] = can_send_other_messages
    if can_add_web_page_previews is not None:
        permissions['can_add_web_page_previews'] = can_add_web_page_previews
    if can_change_info is not None:
        permissions['can_change_info'] = can_change_info
    if can_invite_users is not None:
        permissions['can_invite_users'] = can_invite_users
    if can_pin_messages is not None:
        permissions['can_pin_messages'] = can_pin_messages
    permissions_json = json.dumps(permissions)
    payload = {'chat_id': chat_id, 'user_id': user_id,
               'permissions': permissions_json}
    if until_date is not None:
        if isinstance(until_date, datetime):
            payload['until_date'] = until_date.timestamp()
        else:
            payload['until_date'] = until_date
    return _make_request(token, method_url, params=payload, method='post')


def promote_chat_member(
        token, chat_id, user_id, can_change_info=None, can_post_messages=None,
        can_edit_messages=None, can_delete_messages=None, can_invite_users=None,
        can_restrict_members=None, can_pin_messages=None, can_promote_members=None,
        is_anonymous=None, can_manage_chat=None, can_manage_voice_chats=None):
    method_url = 'promoteChatMember'
    payload = {'chat_id': chat_id, 'user_id': user_id}
    if can_change_info is not None:
        payload['can_change_info'] = can_change_info
    if can_post_messages is not None:
        payload['can_post_messages'] = can_post_messages
    if can_edit_messages is not None:
        payload['can_edit_messages'] = can_edit_messages
    if can_delete_messages is not None:
        payload['can_delete_messages'] = can_delete_messages
    if can_invite_users is not None:
        payload['can_invite_users'] = can_invite_users
    if can_restrict_members is not None:
        payload['can_restrict_members'] = can_restrict_members
    if can_pin_messages is not None:
        payload['can_pin_messages'] = can_pin_messages
    if can_promote_members is not None:
        payload['can_promote_members'] = can_promote_members
    if is_anonymous is not None:
        payload['is_anonymous'] = is_anonymous
    if can_manage_chat is not None:
        payload['can_manage_chat'] = can_manage_chat
    if can_manage_voice_chats is not None:
        payload['can_manage_voice_chats'] = can_manage_voice_chats
    return _make_request(token, method_url, params=payload, method='post')


def set_chat_administrator_custom_title(token, chat_id, user_id, custom_title):
    method_url = 'setChatAdministratorCustomTitle'
    payload = {
        'chat_id': chat_id, 'user_id': user_id, 'custom_title': custom_title
    }
    return _make_request(token, method_url, params=payload, method='post')


def ban_chat_sender_chat(token, chat_id, sender_chat_id):
    method_url = 'banChatSenderChat'
    payload = {'chat_id': chat_id, 'sender_chat_id': sender_chat_id}
    return _make_request(token, method_url, params=payload, method='post')


def unban_chat_sender_chat(token, chat_id, sender_chat_id):
    method_url = 'unbanChatSenderChat'
    payload = {'chat_id': chat_id, 'sender_chat_id': sender_chat_id}
    return _make_request(token, method_url, params=payload, method='post')


def set_chat_permissions(token, chat_id, permissions):
    method_url = 'setChatPermissions'
    payload = {
        'chat_id': chat_id,
        'permissions': permissions.to_json()
    }
    return _make_request(token, method_url, params=payload, method='post')


def create_chat_invite_link(token, chat_id, name, expire_date, member_limit, creates_join_request):
    method_url = 'createChatInviteLink'
    payload = {
        'chat_id': chat_id
    }

    if expire_date is not None:
        if isinstance(expire_date, datetime):
            payload['expire_date'] = expire_date.timestamp()
        else:
            payload['expire_date'] = expire_date
    if member_limit:
        payload['member_limit'] = member_limit
    if creates_join_request is not None:
        payload['creates_join_request'] = creates_join_request
    if name:
        payload['name'] = name

    return _make_request(token, method_url, params=payload, method='post')


def edit_chat_invite_link(token, chat_id, invite_link, name, expire_date, member_limit, creates_join_request):
    method_url = 'editChatInviteLink'
    payload = {
        'chat_id': chat_id,
        'invite_link': invite_link
    }

    if expire_date is not None:
        if isinstance(expire_date, datetime):
            payload['expire_date'] = expire_date.timestamp()
        else:
            payload['expire_date'] = expire_date

    if member_limit is not None:
        payload['member_limit'] = member_limit
    if name:
        payload['name'] = name
    if creates_join_request is not None:
        payload['creates_join_request'] = creates_join_request

    return _make_request(token, method_url, params=payload, method='post')


def revoke_chat_invite_link(token, chat_id, invite_link):
    method_url = 'revokeChatInviteLink'
    payload = {
        'chat_id': chat_id,
        'invite_link': invite_link
    }
    return _make_request(token, method_url, params=payload, method='post')


def export_chat_invite_link(token, chat_id):
    method_url = 'exportChatInviteLink'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload, method='post')


def approve_chat_join_request(token, chat_id, user_id):
    method_url = 'approveChatJoinRequest'
    payload = {
        'chat_id': chat_id,
        'user_id': user_id
    }
    return _make_request(token, method_url, params=payload, method='post')


def decline_chat_join_request(token, chat_id, user_id):
    method_url = 'declineChatJoinRequest'
    payload = {
        'chat_id': chat_id,
        'user_id': user_id
    }
    return _make_request(token, method_url, params=payload, method='post')


def set_chat_photo(token, chat_id, photo):
    method_url = 'setChatPhoto'
    payload = {'chat_id': chat_id}
    files = None
    if is_string(photo):
        payload['photo'] = photo
    elif is_pil_image(photo):
        files = {'photo': pil_image_to_file(photo)}
    else:
        files = {'photo': photo}
    return _make_request(token, method_url, params=payload, files=files, method='post')


def delete_chat_photo(token, chat_id):
    method_url = 'deleteChatPhoto'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload, method='post')


def set_chat_title(token, chat_id, title):
    method_url = 'setChatTitle'
    payload = {'chat_id': chat_id, 'title': title}
    return _make_request(token, method_url, params=payload, method='post')


def get_my_commands(token, scope=None, language_code=None):
    method_url = r'getMyCommands'
    payload = {}
    if scope:
        payload['scope'] = scope.to_json()
    if language_code:
        payload['language_code'] = language_code
    return _make_request(token, method_url, params=payload)


def set_my_commands(token, commands, scope=None, language_code=None):
    method_url = r'setMyCommands'
    payload = {'commands': _convert_list_json_serializable(commands)}
    if scope:
        payload['scope'] = scope.to_json()
    if language_code:
        payload['language_code'] = language_code
    return _make_request(token, method_url, params=payload, method='post')


def delete_my_commands(token, scope=None, language_code=None):
    method_url = r'deleteMyCommands'
    payload = {}
    if scope:
        payload['scope'] = scope.to_json()
    if language_code:
        payload['language_code'] = language_code
    return _make_request(token, method_url, params=payload, method='post')


def set_chat_description(token, chat_id, description):
    method_url = 'setChatDescription'
    payload = {'chat_id': chat_id}
    if description is not None:  # Allow empty strings
        payload['description'] = description
    return _make_request(token, method_url, params=payload, method='post')


def pin_chat_message(token, chat_id, message_id, disable_notification=None):
    method_url = 'pinChatMessage'
    payload = {'chat_id': chat_id, 'message_id': message_id}
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    return _make_request(token, method_url, params=payload, method='post')


def unpin_chat_message(token, chat_id, message_id):
    method_url = 'unpinChatMessage'
    payload = {'chat_id': chat_id}
    if message_id:
        payload['message_id'] = message_id
    return _make_request(token, method_url, params=payload, method='post')


def unpin_all_chat_messages(token, chat_id):
    method_url = 'unpinAllChatMessages'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload, method='post')
