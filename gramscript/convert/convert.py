try:
    import ujson as json
except ImportError:
    import json

from gramscript.types import types


def _convert_list_json_serializable(results):
    ret = ''
    for r in results:
        if isinstance(r, JsonSerializable):
            ret = ret + r.to_json() + ','
    if len(ret) > 0:
        ret = ret[:-1]
    return f'[{ret}]'


def _convert_markup(markup):
    if isinstance(markup, JsonSerializable):
        return markup.to_json()
    return markup


def _convert_entites(entites):
    if entites is None:
        return None
    elif len(entites) == 0:
        return []
    elif isinstance(entites[0], JsonSerializable):
        return [entity.to_json() for entity in entites]
    else:
        return entites


def _convert_poll_options(poll_options):
    if poll_options is None:
        return None
    elif len(poll_options) == 0:
        return []
    elif isinstance(poll_options[0], str):
        # Compatibility mode with previous bug when only list of string was accepted as poll_options
        return poll_options
    elif isinstance(poll_options[0], PollOption):
        return [option.text for option in poll_options]
    else:
        return poll_options


def convert_input_media(media):
    if isinstance(media, InputMedia):
        return media.convert_input_media()
    return None, None


def convert_input_media_array(array):
    media = []
    files = {}
    for input_media in array:
        if isinstance(input_media, InputMedia):
            media_dict = input_media.to_dict()
            if media_dict['media'].startswith('attach://'):
                key = media_dict['media'].replace('attach://', '')
                files[key] = input_media.media
            media.append(media_dict)
    return json.dumps(media), files
