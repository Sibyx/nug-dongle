import logging
from asyncio import Protocol, Transport
from typing import Optional


class DongleServer(Protocol):
    def __init__(self):
        self._client: Optional[Transport] = None

    def connection_made(self, transport: Transport):
        self._client = transport
        peer_name = transport.get_extra_info('peername')
        logging.info(f"Connection from %s:%d", peer_name[0], peer_name[1])
        # TODO: ak si video tak zacni RTP stream

    def data_received(self, data):
        message = data.decode('ascii')
        logging.debug('Received: %s', message.encode().hex())

    def connection_lost(self, exc):
        logging.info("Connection lost: %s", exc)

