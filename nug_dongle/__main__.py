import argparse
import asyncio
import logging
from ipaddress import ip_address
from typing import List
import hid

from zeroconf import ServiceInfo, Zeroconf, IPVersion

from nug_dongle import version
from nug_dongle.server import DongleServer
from .version import __version__


async def serve(hosts: List[str], port: int):
    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda: DongleServer(), hosts, port)
    logging.info("Biding to %s on TCP port %d", ', '.join(hosts), port)

    async with server:
        await server.serve_forever()


def main():
    # Parsing CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-level', type=str, choices=logging._nameToLevel.keys(), default='INFO')
    parser.add_argument('--port', '-p', type=int, default=6700)
    parser.add_argument(
        '--bind', '-b', type=ip_address, default=[ip_address('127.0.0.1'), ip_address('::1')], nargs='+'
    )
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--skip-zeroconf', action='store_true')
    args = parser.parse_args()

    logging.getLogger().setLevel(args.log_level)
    if args.verbose:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d]: %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S%z'
        ))
        logging.getLogger().addHandler(stream_handler)

    logging.info("Loading Nug dongle server %s", version.__version__)

    # Zero-conf
    info = ServiceInfo(
        "_iodongle._tcp.local.",
        "_dongle._iodongle._tcp.local.",
        addresses=[item.packed for item in args.bind],
        port=args.port,
        properties={
            'version': __version__,
            'devices': ('keyboard', 'mouse', 'video')
        },
        server="nug.local.",
    )
    zeroconf = Zeroconf(ip_version=IPVersion.V6Only)

    if not args.skip_zeroconf:
        logging.info("Registration of service using zeroconf")
        zeroconf.register_service(info)

    # https://gist.github.com/davesteele/276a17315cff728bb5932c59329da850
    print(hid.enumerate())

    # asyncio.run(serve(list(map(str, args.bind)), args.port))


if __name__ == '__main__':
    main()
