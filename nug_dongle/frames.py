from nug_dongle.core.frames import fields
from nug_dongle.core.frames.base import Frame


class StartStream(Frame):
    width = fields.U16()
    height = fields.U16()
    name = fields.StringField(header=fields.U8())


class KeyEvent(Frame):
    down = fields.U8()
    key = fields.U32()


class PointerEvent(Frame):
    buttons = fields.U8()
    x = fields.U16()
    y = fields.U16()
