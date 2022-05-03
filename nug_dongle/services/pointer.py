import logging
from pathlib import Path


class HIDService:
    POINTER_MAX_HID = 32767.0

    # Adaptation from
    # https://github.com/tiny-pilot/tinypilot/blob/9fb2e24f7696eb7a03b65aab5220159be9d7707c/app/hid/mouse.py
    def __init__(self, config: dict):
        self._path = Path(config['device'])

    def _write(self, buffer: bytearray):
        logging.debug("Writing to %s: %s", self._path, buffer.hex(' '))
        with open(self._path, 'ab+') as fp:
            fp.write(buffer)

    def _scale_mouse_coordinates(self, relative_x, relative_y):
        x = int(relative_x * self.POINTER_MAX_HID)
        y = int(relative_y * self.POINTER_MAX_HID)
        return x, y

    def pointer(self, x: int, y: int, buttons: int):
        buffer = bytearray([0] * 7)

        x, y = self._scale_mouse_coordinates(x / 1280, y / 1024)

        buffer[0] = buttons
        buffer[1] = x & 0xff
        buffer[2] = (x >> 8) & 0xff
        buffer[3] = y & 0xff
        buffer[4] = (y >> 8) & 0xff
        buffer[5] = 0 & 0xff  # Wheel (not supported)
        buffer[6] = 0 & 0xff  # Wheel (not supported0

        self._write(buffer)
