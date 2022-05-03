from enum import Enum
from typing import Optional

from nug_dongle.services.pointer import HIDService
from nug_dongle.services.video import VideoService


class ServiceType(Enum):
    KEYBOARD = 'keyboard'
    VIDEO = 'video'
    POINTER = 'pointer'


class ServiceContainer:
    def __init__(self, config: dict):
        self._video = None
        self._keyboard = None
        self._pointer = None

        if 'video' in config['services']:
            self._video = VideoService(config['services']['video'])

        if 'pointer' in config['services']:
            self._pointer = HIDService(config['services']['pointer'])

    @property
    def video(self) -> Optional[VideoService]:
        return self._video

    @property
    def pointer(self) -> Optional[HIDService]:
        return self._pointer
