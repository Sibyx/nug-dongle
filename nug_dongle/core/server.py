import asyncio
from asyncio import Protocol, Transport

import logging
from enum import IntEnum
from io import BytesIO

from nug_dongle.core.container import ServiceContainer
from nug_dongle.core.context import Context
from nug_dongle.frames import StartStream, StopStream


class DongleServer(Protocol):
    class MessageType(IntEnum):
        START_STREAM = 1
        STOP_STREAM = 2
        POINTER_EVENT = 3
        KEY_EVENT = 4

    def __init__(self, config: dict, services: ServiceContainer):
        self._context = Context(config)
        self._services = services

    def connection_made(self, transport: Transport):
        self._context.transport = transport
        logging.debug(
            "Making connection with %s:%d (context=%s)", *transport.get_extra_info('peername'), self._context
        )

    def data_received(self, data: bytes):
        logging.debug("Received: %s (context=%s,data=%s)", data.hex(), self._context, data.hex())
        buffer = BytesIO(data)
        match self.MessageType(data[0]):
            case self.MessageType.START_STREAM:
                logging.debug("Received START_STREAM message (context=%s)", self._context)
                payload = StartStream()
                payload.read(buffer)
                self._services.video.start(payload['width'], payload['height'], "vnc-nug-server")
            case self.MessageType.STOP_STREAM:
                logging.debug("Received STOP_STREAM message (context=%s)", self._context)
                payload = StopStream()
                payload.read(buffer)
                self._services.video.stop()
            case self.MessageType.POINTER_EVENT:
                pass
            case self.MessageType.KEY_EVENT:
                pass

    def connection_lost(self, exc: BaseException):
        logging.debug("Connection lost (context=%s)", self._context)

    @classmethod
    async def factory(cls, config: dict, services: ServiceContainer):
        loop = asyncio.get_running_loop()
        server = await loop.create_server(
            lambda: DongleServer(config, services),
            config['general']['bind'], config['general']['port']
        )
        logging.info("Biding to %s on TCP port %d", ', '.join(config['general']['bind']), config['general']['port'])

        async with server:
            await server.serve_forever()
