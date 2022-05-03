import asyncio
import struct
from asyncio import Protocol, StreamReader, StreamWriter

import logging
from enum import IntEnum

from nug_dongle.core.container import ServiceContainer
from nug_dongle.core.context import Context
from nug_dongle import frames


class DongleServer(Protocol):
    class MessageType(IntEnum):
        START_STREAM = 1
        STOP_STREAM = 2
        POINTER_EVENT = 3
        KEY_EVENT = 4

        @classmethod
        def parse(cls, value: bytes):
            data = struct.unpack("B", value)[0]
            return cls(data)

    def __init__(self, config: dict, services: ServiceContainer):
        self.context = Context(config)
        self._services = services

    async def handle(self):
        cmd = await self.context.reader.read(1)
        if not cmd:
            return

        try:
            frame_type = self.MessageType.parse(cmd)
        except ValueError:
            logging.error("Invalid frame type received")
            return

        logging.debug("Received frame type: %s", frame_type)

        match frame_type:
            case self.MessageType.START_STREAM:
                logging.debug("Received START_STREAM message (context=%s)", self.context)
                payload = frames.StartStream()
                await payload.read(self.context.reader)
                self._services.video.start(payload['width'].value, payload['height'].value, "vnc-nug-server")
                logging.debug("Started VideoService (context=%s)", self.context)
            case self.MessageType.STOP_STREAM:
                logging.debug("Received STOP_STREAM message (context=%s)", self.context)
                self._services.video.stop()
            case self.MessageType.POINTER_EVENT:
                payload = frames.PointerEvent()
                await payload.read(self.context.reader)
                logging.debug(
                    "Received POINTER_EVENT message (context=%s,x=%s,y=%s)",
                    self.context, payload.x.value, payload.y.value
                )
                self._services.pointer.pointer(payload.x.value, payload.y.value, payload.buttons.value)
            case self.MessageType.KEY_EVENT:
                payload = frames.KeyEvent()
                await payload.read(self.context.reader)
                logging.debug(
                    "Received KEY_EVENT message (context=%s,down=%s,key=%s)",
                    self.context, payload.down.value, payload.key.value
                )

    async def __call__(self, reader: StreamReader, writer: StreamWriter):
        self.context.reader = reader
        self.context.writer = writer

        logging.debug(
            "Making connection with %s:%d (context=%s)", *writer.get_extra_info('peername'), self.context
        )

        while not self.context.reader.at_eof():
            await self.handle()
        else:
            logging.debug("Connection lost (context=%s)", self.context)

    @classmethod
    async def factory(cls, config: dict, services: ServiceContainer):
        server = await asyncio.start_server(
            DongleServer(config, services),
            config['general']['bind'],
            config['general']['port']
        )
        logging.info("Biding to %s on TCP port %d", ', '.join(config['general']['bind']), config['general']['port'])

        async with server:
            await server.serve_forever()
