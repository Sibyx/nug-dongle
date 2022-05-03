from enum import Enum
from typing import Optional

from nug_dongle.services.video import VideoService


class ServiceType(Enum):
    KEYBOARD = 'keyboard'
    VIDEO = 'video'
    POINTER = 'pointer'


class ServiceContainer:
    def __init__(self, config: dict):
        self._video = None
        self._keyboard = None
        self._mouse = None

        if 'video' in config['services']:
            self._video = VideoService(config['services']['video'])

    @property
    def video(self) -> Optional[VideoService]:
        return self._video
