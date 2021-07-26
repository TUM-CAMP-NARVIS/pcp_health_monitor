import sys
import asyncio
import zmq
import zmq.asyncio
import logging
import argparse

from parse_config import parse_config
from health_monitor.monitor import MonitorService


def parse_args():
    parser = argparse.ArgumentParser(usage='Connects to the capture server.')
    parser.add_argument("-c", "--config", required=True,
                        help="Path to the yaml config file for the hosts of the current setup")  # noqa
    return parser.parse_args()


def setup_application(hosts, enable_telegram=False):
    loop = asyncio.get_event_loop()
    ctx = zmq.asyncio.Context()

    ms = MonitorService()
    logging.debug("Initializing monitor service")
    loop.run_until_complete(ms.initialize(enable_telegram))

    try:
        for host, data in hosts.items():
            ip = data["hostname"]
            port = data["port"]
            loop.run_until_complete(ms.register_node(ctx, host, ip, port))
        loop.run_until_complete(ms.monitor())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
            format='%(levelname)7s: %(message)s',
            stream=sys.stderr)
    logging.getLogger("asyncio").setLevel(logging.INFO)
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)
    config_file = parse_args().config
    config = parse_config(config_file)
    setup_application(config["hosts"], config.get("enable_telegram"))
