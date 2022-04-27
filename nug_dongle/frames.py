from nug_dongle.core.frames import fields
from nug_dongle.core.frames.base import Frame


class StartStream(Frame):
    type = fields.U8()
    width = fields.U16()
    height = fields.U16()
    # name = fields.ArrayField(fields.StructField('c'), header=fields.U8())


class StopStream(Frame):
    type = fields.U8()
