from asyncio import Transport
from typing import Optional
from uuid import uuid4, UUID


class Context:
    def __init__(self, config: dict):
        self._id = uuid4()
        self._config = config
        self._transport = None

    def __str__(self):
        return str(self._id)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def transport(self) -> Optional[Transport]:
        return self._transport

    @transport.setter
    def transport(self, value: Transport):
        self._transport = value

    @property
    def config(self) -> dict:
        return self._config
