from asyncio import StreamReader, StreamWriter
from uuid import uuid4, UUID


class Context:
    def __init__(self, config: dict):
        self._id = uuid4()
        self._config = config
        self._reader = None
        self._writer = None

    def __str__(self):
        return str(self._id)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def reader(self) -> StreamReader:
        return self._reader

    @reader.setter
    def reader(self, value: StreamReader):
        self._reader = value

    @property
    def writer(self) -> StreamWriter:
        return self._writer

    @writer.setter
    def writer(self, value: StreamWriter):
        self._writer = value

    @property
    def config(self) -> dict:
        return self._config
