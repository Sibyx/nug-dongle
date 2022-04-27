from subprocess import Popen
from typing import Optional


class VideoService:
    def __init__(self, config: dict):
        self._process: Optional[Popen] = None
        self._config = config
        self._stdout = None
        self._stderr = None

    def start(self, width: int, height: int, stream_name: str):
        if not self._process:
            if self._config.get('stdout'):
                self._stdout = open(self._config['stdout'], 'a+')

            if self._config.get('stderr', 'a+'):
                self._stderr = open(self._config['stderr'])

            # FIXME: Not working properly (WTF)
            self._process = Popen(
                " ".join([
                    'ffmpeg', '-i', self._config['device'], '-s', f'{width}x{height}', '-input_format', 'mjpeg',
                    '-c:v', 'mjpeg', '-f', 'v4l2', '-pix_fmt', 'yuvj420p', '-vcodec', 'mjpeg', '-huffman', '0',
                    '-f', 'rtsp', '-rtsp_transport', 'tcp', f"rtsp://{self._config['server']}/{stream_name}"
                ]),
                stdout=self._stdout,
                stderr=self._stderr,
                shell=True
            )

    def stop(self):
        if self._process:
            self._process.kill()
