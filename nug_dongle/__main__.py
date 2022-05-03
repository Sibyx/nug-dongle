import argparse
import asyncio
import logging
from ipaddress import ip_address
from logging.handlers import SysLogHandler
from pathlib import Path

import tomli as tomli

from zeroconf import ServiceInfo, Zeroconf, IPVersion

from nug_dongle import version
from nug_dongle.core.container import ServiceContainer
from nug_dongle.core.server import DongleServer


if __name__ == '__main__':
    # Parsing CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--config', '-c', type=Path)
    args = parser.parse_args()

    # Read config file
    with open(args.config, "rb") as f:
        config = tomli.load(f)

    # Set loglevel
    logging.getLogger().setLevel(config['general'].get('log_level', 'INFO'))

    if 'syslog' in config:
        handler = SysLogHandler(address=(config['syslog']['ip'], config['syslog']['port']))
        logging.getLogger().addHandler(handler)

    if args.verbose:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d]: %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S%z'
        ))
        logging.getLogger().addHandler(stream_handler)

    logging.info("Loading Nug dongle server %s", version.__version__)

    # Zero-conf
    if config.get('zeroconf'):
        logging.info("Registration of service using zeroconf")
        info = ServiceInfo(
            "_nug-ghoul._tcp.local.",
            f"{config['zeroconf'].get('name', '_dongle')}._nug-ghoul._tcp.local.",
            addresses=[ip_address(item).packed for item in config['general']['bind']],
            port=config['general']['port'],
            properties={
                'version': version.__version__,
                'services': list(config['services'].keys())
            },
        )
        zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
        zeroconf.register_service(info)
    else:
        zeroconf = None
        info = None

    # https://gist.github.com/davesteele/276a17315cff728bb5932c59329da850

    services = ServiceContainer(config)

    try:
        asyncio.run(
            DongleServer.factory(config, services)
        )
    except KeyboardInterrupt:
        if zeroconf:
            logging.info("Unregister zeroconf services")
            zeroconf.unregister_service(info)
            zeroconf.close()
            exit(0)
