import asyncio
from asyncio import Protocol, Transport

import logging

from nug_dongle.core.context import Context


class DongleServer(Protocol):
    def __init__(self, config: dict):
        self._context = Context(config)

    def connection_made(self, transport: Transport):
        self._context.transport = transport
        logging.debug(
            "Making connection with %s:%d (context=%s)", *transport.get_extra_info('peername'), self._context
        )

    def data_received(self, data: bytes):
        logging.debug("Received: %s (context=%s,data=%s)", data.hex(), self._context, data.hex())

    def connection_lost(self, exc: BaseException):
        logging.debug("Connection lost (context=%s)", self._context)

    @classmethod
    async def factory(cls, config: dict):
        loop = asyncio.get_running_loop()
        server = await loop.create_server(
            lambda: DongleServer(config),
            config['general']['bind'], config['general']['port']
        )
        logging.info("Biding to %s on TCP port %d", ', '.join(config['general']['bind']), config['general']['port'])

        async with server:
            await server.serve_forever()
