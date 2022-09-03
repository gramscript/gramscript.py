

from gramscript.api import types


class ChatAction:
    """This class provides a convenient access to all Chat Actions available.
    It is intended to be used with :obj:`gramscript.Client.send_chat_action`.
    """

    CANCEL = types.SendMessageCancelAction
    """Cancels any chat action currently displayed."""

    TYPING = types.SendMessageTypingAction
    """User is typing a text message."""

    PLAYING = types.SendMessageGamePlayAction
    """User is playing a game."""

    CHOOSE_CONTACT = types.SendMessageChooseContactAction
    """User is choosing a contact to share."""

    UPLOAD_PHOTO = types.SendMessageUploadPhotoAction
    """User is uploading a photo."""

    RECORD_VIDEO = types.SendMessageRecordVideoAction
    """User is recording a video."""

    UPLOAD_VIDEO = types.SendMessageUploadVideoAction
    """User is uploading a video."""

    RECORD_AUDIO = types.SendMessageRecordAudioAction
    """User is recording an audio message."""

    UPLOAD_AUDIO = types.SendMessageUploadAudioAction
    """User is uploading an audio message."""

    UPLOAD_DOCUMENT = types.SendMessageUploadDocumentAction
    """User is uploading a generic document."""

    FIND_LOCATION = types.SendMessageGeoLocationAction
    """User is searching for a location on the map."""

    RECORD_VIDEO_NOTE = types.SendMessageRecordRoundAction
    """User is recording a round video note."""

    UPLOAD_VIDEO_NOTE = types.SendMessageUploadRoundAction
    """User is uploading a round video note."""
