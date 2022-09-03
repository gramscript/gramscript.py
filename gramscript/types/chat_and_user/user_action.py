from datetime import datetime
from gramscript.asyncio.helper import _convert_poll_options
from gramscript.convert.convert import _convert_entites, _convert_markup, convert_input_media, convert_input_media_array
from gramscript.request import _make_request
from gramscript.types.chat_and_user.chat_action import get_method_by_type
from gramscript.util import is_pil_image, is_string, pil_image_to_file


try:
    import ujson as json
except ImportError:
    import json


def forward_message(
        token, chat_id, from_chat_id, message_id,
        disable_notification=None, timeout=None, protect_content=None):
    method_url = r'forwardMessage'
    payload = {'chat_id': chat_id,
               'from_chat_id': from_chat_id, 'message_id': message_id}
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if timeout:
        payload['timeout'] = timeout
    if protect_content is not None:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload)


def copy_message(token, chat_id, from_chat_id, message_id, caption=None, parse_mode=None, caption_entities=None,
                 disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None,
                 reply_markup=None, timeout=None, protect_content=None):
    method_url = r'copyMessage'
    payload = {'chat_id': chat_id,
               'from_chat_id': from_chat_id, 'message_id': message_id}
    if caption is not None:
        payload['caption'] = caption
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if caption_entities is not None:
        payload['caption_entities'] = _convert_entites(caption_entities)
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup is not None:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if timeout:
        payload['timeout'] = timeout
    if protect_content is not None:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload)


def send_message(
        token, chat_id, text,
        disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
        parse_mode=None, disable_notification=None, timeout=None,
        entities=None, allow_sending_without_reply=None, protect_content=None):
    """
    Use this method to send text messages. On success, the sent Message is returned.
    :param token:
    :param chat_id:
    :param text:
    :param disable_web_page_preview:
    :param reply_to_message_id:
    :param reply_markup:
    :param parse_mode:
    :param disable_notification:
    :param timeout:
    :param entities:
    :param allow_sending_without_reply:
    :return:
    """
    method_url = r'sendMessage'
    payload = {'chat_id': str(chat_id), 'text': text}
    if disable_web_page_preview is not None:
        payload['disable_web_page_preview'] = disable_web_page_preview
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if timeout:
        payload['timeout'] = timeout
    if entities:
        payload['entities'] = json.dumps(
            MessageEntity.to_list_of_dicts(entities))
    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if protect_content is not None:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload, method='post')


def send_poll(
        token, chat_id,
        question, options,
        is_anonymous=None, type=None, allows_multiple_answers=None, correct_option_id=None,
        explanation=None, explanation_parse_mode=None, open_period=None, close_date=None, is_closed=None,
        disable_notification=False, reply_to_message_id=None, allow_sending_without_reply=None,
        reply_markup=None, timeout=None, explanation_entities=None, protect_content=None):
    method_url = r'sendPoll'
    payload = {
        'chat_id': str(chat_id),
        'question': question,
        'options': json.dumps(_convert_poll_options(options))}

    if is_anonymous is not None:
        payload['is_anonymous'] = is_anonymous
    if type is not None:
        payload['type'] = type
    if allows_multiple_answers is not None:
        payload['allows_multiple_answers'] = allows_multiple_answers
    if correct_option_id is not None:
        payload['correct_option_id'] = correct_option_id
    if explanation is not None:
        payload['explanation'] = explanation
    if explanation_parse_mode is not None:
        payload['explanation_parse_mode'] = explanation_parse_mode
    if open_period is not None:
        payload['open_period'] = open_period
    if close_date is not None:
        if isinstance(close_date, datetime):
            payload['close_date'] = close_date.timestamp()
        else:
            payload['close_date'] = close_date
    if is_closed is not None:
        payload['is_closed'] = is_closed

    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id is not None:
        payload['reply_to_message_id'] = reply_to_message_id
    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup is not None:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if timeout:
        payload['timeout'] = timeout
    if explanation_entities:
        payload['explanation_entities'] = json.dumps(
            MessageEntity.to_list_of_dicts(explanation_entities))
    if protect_content:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload)


def stop_poll(token, chat_id, message_id, reply_markup=None):
    method_url = r'stopPoll'
    payload = {'chat_id': str(chat_id), 'message_id': message_id}
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload)


def get_sticker_set(token, name):
    method_url = 'getStickerSet'
    return _make_request(token, method_url, params={'name': name})


def upload_sticker_file(token, user_id, png_sticker):
    method_url = 'uploadStickerFile'
    payload = {'user_id': user_id}
    files = {'png_sticker': png_sticker}
    return _make_request(token, method_url, params=payload, files=files, method='post')


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


def create_new_sticker_set(
        token, user_id, name, title, emojis, png_sticker, tgs_sticker,
        contains_masks=None, mask_position=None):
    method_url = 'createNewStickerSet'
    payload = {'user_id': user_id, 'name': name,
               'title': title, 'emojis': emojis}
    stype = 'png_sticker' if png_sticker else 'tgs_sticker'
    sticker = png_sticker or tgs_sticker
    files = None
    if not is_string(sticker):
        files = {stype: sticker}
    else:
        payload[stype] = sticker
    if contains_masks is not None:
        payload['contains_masks'] = contains_masks
    if mask_position:
        payload['mask_position'] = mask_position.to_json()
    return _make_request(token, method_url, params=payload, files=files, method='post')


def add_sticker_to_set(token, user_id, name, emojis, png_sticker, tgs_sticker, mask_position):
    method_url = 'addStickerToSet'
    payload = {'user_id': user_id, 'name': name, 'emojis': emojis}
    stype = 'png_sticker' if png_sticker else 'tgs_sticker'
    sticker = png_sticker or tgs_sticker
    files = None
    if not is_string(sticker):
        files = {stype: sticker}
    else:
        payload[stype] = sticker
    if mask_position:
        payload['mask_position'] = mask_position.to_json()
    return _make_request(token, method_url, params=payload, files=files, method='post')


def set_sticker_position_in_set(token, sticker, position):
    method_url = 'setStickerPositionInSet'
    payload = {'sticker': sticker, 'position': position}
    return _make_request(token, method_url, params=payload, method='post')


def delete_sticker_from_set(token, sticker):
    method_url = 'deleteStickerFromSet'
    payload = {'sticker': sticker}
    return _make_request(token, method_url, params=payload, method='post')


def edit_message_text(token, text, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None,
                      entities=None, disable_web_page_preview=None, reply_markup=None):
    method_url = r'editMessageText'
    payload = {'text': text}
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if entities:
        payload['entities'] = json.dumps(
            MessageEntity.to_list_of_dicts(entities))
    if disable_web_page_preview is not None:
        payload['disable_web_page_preview'] = disable_web_page_preview
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, method='post')


def edit_message_caption(token, caption, chat_id=None, message_id=None, inline_message_id=None,
                         parse_mode=None, caption_entities=None, reply_markup=None):
    method_url = r'editMessageCaption'
    payload = {'caption': caption}
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if caption_entities:
        payload['caption_entities'] = json.dumps(
            MessageEntity.to_list_of_dicts(caption_entities))
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, method='post')


def edit_message_media(token, media, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
    method_url = r'editMessageMedia'
    media_json, file = convert_input_media(media)
    payload = {'media': media_json}
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, files=file, method='post' if file else 'get')


def edit_message_reply_markup(token, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
    method_url = r'editMessageReplyMarkup'
    payload = {}
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, method='post')


def delete_message(token, chat_id, message_id, timeout=None):
    method_url = r'deleteMessage'
    payload = {'chat_id': chat_id, 'message_id': message_id}
    if timeout:
        payload['timeout'] = timeout
    return _make_request(token, method_url, params=payload, method='post')


def forward_message(
        token, chat_id, from_chat_id, message_id,
        disable_notification=None, timeout=None, protect_content=None):
    method_url = r'forwardMessage'
    payload = {'chat_id': chat_id,
               'from_chat_id': from_chat_id, 'message_id': message_id}
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if timeout:
        payload['timeout'] = timeout
    if protect_content is not None:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload)


def copy_message(token, chat_id, from_chat_id, message_id, caption=None, parse_mode=None, caption_entities=None,
                 disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None,
                 reply_markup=None, timeout=None, protect_content=None):
    method_url = r'copyMessage'
    payload = {'chat_id': chat_id,
               'from_chat_id': from_chat_id, 'message_id': message_id}
    if caption is not None:
        payload['caption'] = caption
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if caption_entities is not None:
        payload['caption_entities'] = _convert_entites(caption_entities)
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup is not None:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if timeout:
        payload['timeout'] = timeout
    if protect_content is not None:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload)


def send_dice(
        token, chat_id,
        emoji=None, disable_notification=None, reply_to_message_id=None,
        reply_markup=None, timeout=None, allow_sending_without_reply=None, protect_content=None):
    method_url = r'sendDice'
    payload = {'chat_id': chat_id}
    if emoji:
        payload['emoji'] = emoji
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if timeout:
        payload['timeout'] = timeout
    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if protect_content is not None:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload)


def send_photo(
        token, chat_id, photo,
        caption=None, reply_to_message_id=None, reply_markup=None,
        parse_mode=None, disable_notification=None, timeout=None,
        caption_entities=None, allow_sending_without_reply=None, protect_content=None):
    method_url = r'sendPhoto'
    payload = {'chat_id': chat_id}
    files = None
    if is_string(photo):
        payload['photo'] = photo
    elif is_pil_image(photo):
        files = {'photo': pil_image_to_file(photo)}
    else:
        files = {'photo': photo}
    if caption:
        payload['caption'] = caption
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if timeout:
        payload['timeout'] = timeout
    if caption_entities:
        payload['caption_entities'] = json.dumps(
            MessageEntity.to_list_of_dicts(caption_entities))
    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if protect_content is not None:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_media_group(token, chat_id, media, disable_notification=None, reply_to_message_id=None, timeout=None, allow_sending_without_reply=None, protect_content=None):
    method_url = 'sendMediaGroup'
    media_json, files = convert_input_media_array(media)
    payload = {'chat_id': chat_id, 'media': media_json}
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if timeout:
        payload['timeout'] = timeout
    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if protect_content is not None:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload, method='post' if files else 'get', files=files or None)


def send_location(
        token, chat_id, latitude, longitude,
        live_period=None, reply_to_message_id=None,
        reply_markup=None, disable_notification=None,
        timeout=None, horizontal_accuracy=None, heading=None,
        proximity_alert_radius=None, allow_sending_without_reply=None, protect_content=None):
    method_url = r'sendLocation'
    payload = {'chat_id': chat_id,
               'latitude': latitude, 'longitude': longitude}
    if live_period:
        payload['live_period'] = live_period
    if horizontal_accuracy:
        payload['horizontal_accuracy'] = horizontal_accuracy
    if heading:
        payload['heading'] = heading
    if proximity_alert_radius:
        payload['proximity_alert_radius'] = proximity_alert_radius
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if timeout:
        payload['timeout'] = timeout
    if protect_content is not None:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload)


def edit_message_live_location(
        token, latitude, longitude, chat_id=None, message_id=None,
        inline_message_id=None, reply_markup=None, timeout=None,
        horizontal_accuracy=None, heading=None, proximity_alert_radius=None):
    method_url = r'editMessageLiveLocation'
    payload = {'latitude': latitude, 'longitude': longitude}
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if horizontal_accuracy:
        payload['horizontal_accuracy'] = horizontal_accuracy
    if heading:
        payload['heading'] = heading
    if proximity_alert_radius:
        payload['proximity_alert_radius'] = proximity_alert_radius
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if timeout:
        payload['timeout'] = timeout
    return _make_request(token, method_url, params=payload)


def stop_message_live_location(
        token, chat_id=None, message_id=None,
        inline_message_id=None, reply_markup=None, timeout=None):
    method_url = r'stopMessageLiveLocation'
    payload = {}
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if timeout:
        payload['timeout'] = timeout
    return _make_request(token, method_url, params=payload)


def send_venue(
        token, chat_id, latitude, longitude, title, address,
        foursquare_id=None, foursquare_type=None, disable_notification=None,
        reply_to_message_id=None, reply_markup=None, timeout=None,
        allow_sending_without_reply=None, google_place_id=None,
        google_place_type=None, protect_content=None):
    method_url = r'sendVenue'
    payload = {'chat_id': chat_id, 'latitude': latitude,
               'longitude': longitude, 'title': title, 'address': address}
    if foursquare_id:
        payload['foursquare_id'] = foursquare_id
    if foursquare_type:
        payload['foursquare_type'] = foursquare_type
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if timeout:
        payload['timeout'] = timeout
    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if google_place_id:
        payload['google_place_id'] = google_place_id
    if google_place_type:
        payload['google_place_type'] = google_place_type
    if protect_content is not None:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload)


def send_contact(
        token, chat_id, phone_number, first_name, last_name=None, vcard=None,
        disable_notification=None, reply_to_message_id=None, reply_markup=None, timeout=None,
        allow_sending_without_reply=None, protect_content=None):
    method_url = r'sendContact'
    payload = {'chat_id': chat_id,
               'phone_number': phone_number, 'first_name': first_name}
    if last_name:
        payload['last_name'] = last_name
    if vcard:
        payload['vcard'] = vcard
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if timeout:
        payload['timeout'] = timeout
    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if protect_content is not None:
        payload['protect_content'] = protect_content

    return _make_request(token, method_url, params=payload)


def send_chat_action(token, chat_id, action, timeout=None):
    method_url = r'sendChatAction'
    payload = {'chat_id': chat_id, 'action': action}
    if timeout:
        payload['timeout'] = timeout
    return _make_request(token, method_url, params=payload)


def send_video(token, chat_id, data, duration=None, caption=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, supports_streaming=None, disable_notification=None, timeout=None, thumb=None, width=None, height=None, caption_entities=None, allow_sending_without_reply=None, protect_content=None):
    method_url = 'sendVideo'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(data):
        files = {'video': data}
    else:
        payload['video'] = data
    if duration:
        payload['duration'] = duration
    if caption:
        payload['caption'] = caption
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if supports_streaming is not None:
        payload['supports_streaming'] = supports_streaming
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if timeout:
        payload['timeout'] = timeout
    if thumb:
        if is_string(thumb):
            payload['thumb'] = thumb
        elif files:
            files['thumb'] = thumb
        else:
            files = {'thumb': thumb}
    if width:
        payload['width'] = width
    if height:
        payload['height'] = height
    if caption_entities:
        payload['caption_entities'] = json.dumps(
            MessageEntity.to_list_of_dicts(caption_entities))

    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if protect_content is not None:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_animation(token, chat_id, data, duration=None, caption=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None, timeout=None, thumb=None, caption_entities=None, allow_sending_without_reply=None, protect_content=None, width=None, height=None):
    method_url = 'sendAnimation'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(data):
        files = {'animation': data}
    else:
        payload['animation'] = data
    if duration:
        payload['duration'] = duration
    if caption:
        payload['caption'] = caption
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if timeout:
        payload['timeout'] = timeout
    if thumb:
        if is_string(thumb):
            payload['thumb'] = thumb
        elif files:
            files['thumb'] = thumb
        else:
            files = {'thumb': thumb}
    if caption_entities:
        payload['caption_entities'] = json.dumps(
            MessageEntity.to_list_of_dicts(caption_entities))

    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if protect_content is not None:
        payload['protect_content'] = protect_content
    if width:
        payload['width'] = width
    if height:
        payload['height'] = height
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_voice(token, chat_id, voice, caption=None, duration=None, reply_to_message_id=None, reply_markup=None,
               parse_mode=None, disable_notification=None, timeout=None, caption_entities=None,
               allow_sending_without_reply=None, protect_content=None):
    method_url = r'sendVoice'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(voice):
        files = {'voice': voice}
    else:
        payload['voice'] = voice
    if caption:
        payload['caption'] = caption
    if duration:
        payload['duration'] = duration
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if timeout:
        payload['timeout'] = timeout
    if caption_entities:
        payload['caption_entities'] = json.dumps(
            MessageEntity.to_list_of_dicts(caption_entities))
    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if protect_content is not None:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_video_note(token, chat_id, data, duration=None, length=None, reply_to_message_id=None, reply_markup=None, disable_notification=None, timeout=None, thumb=None, allow_sending_without_reply=None, protect_content=None):
    method_url = 'sendVideoNote'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(data):
        files = {'video_note': data}
    else:
        payload['video_note'] = data
    if duration:
        payload['duration'] = duration
    if length and str(length).isdigit() and int(length) <= 639:
        payload['length'] = length
    else:
        payload['length'] = 639
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if timeout:
        payload['timeout'] = timeout
    if thumb:
        if is_string(thumb):
            payload['thumb'] = thumb
        elif files:
            files['thumb'] = thumb
        else:
            files = {'thumb': thumb}
    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if protect_content is not None:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_audio(token, chat_id, audio, caption=None, duration=None, performer=None, title=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None, timeout=None, thumb=None, caption_entities=None, allow_sending_without_reply=None, protect_content=None):
    method_url = 'sendAudio'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(audio):
        files = {'audio': audio}
    else:
        payload['audio'] = audio
    if caption:
        payload['caption'] = caption
    if duration:
        payload['duration'] = duration
    if performer:
        payload['performer'] = performer
    if title:
        payload['title'] = title
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if timeout:
        payload['timeout'] = timeout
    if thumb:
        if is_string(thumb):
            payload['thumb'] = thumb
        elif files:
            files['thumb'] = thumb
        else:
            files = {'thumb': thumb}
    if caption_entities:
        payload['caption_entities'] = json.dumps(
            MessageEntity.to_list_of_dicts(caption_entities))

    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if protect_content is not None:
        payload['protect_content'] = protect_content
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_data(token, chat_id, data, data_type, reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None, timeout=None, caption=None, thumb=None, caption_entities=None, allow_sending_without_reply=None, disable_content_type_detection=None, visible_file_name=None):
    method_url = get_method_by_type(data_type)
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(data):
        file_data = data
        if visible_file_name:
            file_data = visible_file_name, data
        files = {data_type: file_data}
    else:
        payload[data_type] = data
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if parse_mode and data_type == 'document':
        payload['parse_mode'] = parse_mode
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if timeout:
        payload['timeout'] = timeout
    if caption:
        payload['caption'] = caption
    if thumb:
        if is_string(thumb):
            payload['thumb'] = thumb
        elif files:
            files['thumb'] = thumb
        else:
            files = {'thumb': thumb}
    if caption_entities:
        payload['caption_entities'] = json.dumps(
            MessageEntity.to_list_of_dicts(caption_entities))

    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if method_url == 'sendDocument' and disable_content_type_detection is not None:
        payload['disable_content_type_detection'] = disable_content_type_detection
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_game(
        token, chat_id, game_short_name,
        disable_notification=None, reply_to_message_id=None, reply_markup=None, timeout=None,
        allow_sending_without_reply=None, protect_content=None):
    method_url = r'sendGame'
    payload = {'chat_id': chat_id, 'game_short_name': game_short_name}
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if timeout:
        payload['timeout'] = timeout
    if allow_sending_without_reply is not None:
        payload['allow_sending_without_reply'] = allow_sending_without_reply
    if protect_content is not None:
        payload['protect_content'] = protect_content

    return _make_request(token, method_url, params=payload)


# https://core.telegram.org/bots/api#setgamescore
def set_game_score(token, user_id, score, force=None, disable_edit_message=None, chat_id=None, message_id=None,
                   inline_message_id=None):
    """
    Use this method to set the score of the specified user in a game. On success, if the message was sent by the bot, returns the edited Message, otherwise returns True. Returns an error, if the new score is not greater than the user's current score in the chat.
    :param token: Bot's token (you don't need to fill this)
    :param user_id: User identifier
    :param score: New score, must be non-negative
    :param force: (Optional) Pass True, if the high score is allowed to decrease. This can be useful when fixing mistakes or banning cheaters
    :param disable_edit_message: (Optional) Pass True, if the game message should not be automatically edited to include the current scoreboard
    :param chat_id: (Optional, required if inline_message_id is not specified) Unique identifier for the target chat (or username of the target channel in the format @channelusername)
    :param message_id: (Optional, required if inline_message_id is not specified) Unique identifier of the sent message
    :param inline_message_id: (Optional, required if chat_id and message_id are not specified) Identifier of the inline message
    :return:
    """
    method_url = r'setGameScore'
    payload = {'user_id': user_id, 'score': score}
    if force is not None:
        payload['force'] = force
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    if disable_edit_message is not None:
        payload['disable_edit_message'] = disable_edit_message
    return _make_request(token, method_url, params=payload)


# https://core.telegram.org/bots/api#getgamehighscores
def get_game_high_scores(token, user_id, chat_id=None, message_id=None, inline_message_id=None):
    """
    Use this method to get data for high score tables. Will return the score of the specified user and several of his neighbors in a game. On success, returns an Array of GameHighScore objects.
    This method will currently return scores for the target user, plus two of his closest neighbors on each side. Will also return the top three users if the user and his neighbors are not among them. Please note that this behavior is subject to change.
    :param token: Bot's token (you don't need to fill this)
    :param user_id: Target user id
    :param chat_id: (Optional, required if inline_message_id is not specified) Unique identifier for the target chat (or username of the target channel in the format @channelusername)
    :param message_id: (Optional, required if inline_message_id is not specified) Unique identifier of the sent message
    :param inline_message_id: (Optional, required if chat_id and message_id are not specified) Identifier of the inline message
    :return:
    """
    method_url = r'getGameHighScores'
    payload = {'user_id': user_id}
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    return _make_request(token, method_url, params=payload)
