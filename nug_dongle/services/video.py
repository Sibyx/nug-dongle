import logging
from subprocess import Popen
from typing import Optional


class VideoService:
    def __init__(self, config: dict):
        self._process: Optional[Popen] = None
        self._config = config

    def start(self, width: int, height: int, stream_name: str):
        if not self._process:
            with open(self._config['stdout'], "ab") as out, open(self._config['stderr'], "ab") as err:
                self._process = Popen(
                    " ".join([
                        'ffmpeg', '-i', self._config['device'], '-s', f'{width}x{height}', '-input_format', 'mjpeg',
                        '-c:v', 'mjpeg', '-f', 'v4l2', '-pix_fmt', 'yuvj420p', '-vcodec', 'mjpeg', '-huffman', '0',
                        '-f', 'rtsp', '-rtsp_transport', 'tcp', f"rtsp://{self._config['server']}/{stream_name}"
                    ]),
                    stdout=out,
                    stderr=err,
                    shell=True
                )
                logging.debug("Started ffmpeg with PID %d", self._process.pid)

    def stop(self):
        if self._process:
            self._process.kill()
