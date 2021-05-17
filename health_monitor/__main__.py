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


def setup_application(host):
    loop = asyncio.get_event_loop()
    ctx = zmq.asyncio.Context()

    ms = MonitorService()

    try:
        for host in hosts:
            socket = ctx.socket(zmq.SUB)
            hostname = host["monitor"]["hostname"]
            port = host["monitor"]["port"]
            socket.bind(f'tcp://{hostname}:{port}')
            socket.setsockopt_string(zmq.SUBSCRIBE, '')
            logging.info(f"Starting monitor for node {hostname}")
            asyncio.ensure_future(ms.monitor(socket))
        asyncio.ensure_future(ms.process_events())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    config = parse_args().config
    hosts = parse_config(config)['site']['hosts']
    setup_application(hosts)
