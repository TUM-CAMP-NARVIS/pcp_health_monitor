import asyncio
import zmq
import zmq.asyncio
import logging
from datetime import datetime

import numpy as np

from health_monitor.telegram_client import initialize_telegram_bot, message_all_users
import schemata as schema

logger = logging.getLogger(__name__)


class MonitorService(object):

    telegram_enabled = False

    nodes = []
    # access shared state
    brightness_events = []
    fps_events = []

    async def initialize(self, telegram):
        self.telegram_enabled = telegram
        if self.telegram_enabled:
            await initialize_telegram_bot()


    async def register_node(self, ctx, hostname, ip, port):
        socket = ctx.socket(zmq.SUB)
        connection_string = f'tcp://{ip}:{port}'
        logger.info("Connecting to: " + connection_string)
        socket.connect(connection_string)
        socket.setsockopt_string(zmq.SUBSCRIBE, '')
        logger.info(f"Starting monitor for node {hostname}")
        node = ComputeNode(hostname, socket)
        self.nodes.append(node)

    async def monitor(self):
        # initialize the listening tasks
        for node in self.nodes:
            loop = asyncio.get_event_loop()
            loop.create_task(node.listen())
        while True:
            # once per minute, process events
            await asyncio.sleep(60)
            # TODO: run in a new thread so we don't
            # block new events from incoming?
            summary = await self.process_events()
            logger.info(f"Detection summary: \n {summary}")
            if self.telegram_enabled:
                await message_all_users(summary)

    async def process_events(self):
        summary = ""
        for node in self.nodes:
            summary += node.generate_summary()
        return summary


class ComputeNode(object):

    hostname = None

    def __init__(self, hostname, socket):
        self.hostname = hostname
        self.socket = socket
        self.frame_rate = []
        self.imu_errors = 0
        self.last_sent_imu = datetime.now()

    async def listen(self):
        while True:
            msg = await self.socket.recv()
            event = schema.events.ApplicationEvent.from_bytes(msg)
            logger.debug(f"Recieved info from {self.hostname} \n {event}")
            await self._process_event(event)

    def generate_summary(self):
        summary = f"""node: {self.hostname}
        Num Frames: {np.sum(self.frame_rate)}
        Average Frame Rate: {np.mean(self.frame_rate):.2f}
        # Imu Errors: {self.imu_errors}
        """

        self.frame_rate = []
        self.imu_errors = 0
        return summary

    async def _process_event(self, event):
        if is_frame_rate_info(event):
            data = np.frombuffer(event.event.value.healthStatus.payload, np.uint8)
            if len(data) > 0:
                framerate = data[0]
                logger.debug(f"{self.hostname} recording at {framerate} fps")
                self.frame_rate.append(framerate)

        if is_imu_movement(event):
            logger.info(f"{self.hostname}: imuMovement")
            self.imu_errors += 1
            if (datetime.now() - self.last_sent_imu).total_seconds() > 10.0:
                await message_all_users(f"{self.hostname}: imu movement error!", disable_notifications=False)
                self.last_sent_imu = datetime.now()


def is_frame_rate_info(event):
    return event.event.value.healthStatus.healthStatus == schema.events.HealthStatusUpdate.frameRateInfo


def is_imu_movement(event):
    return event.event.value.healthStatus.healthStatus == schema.events.HealthStatusUpdate.imuMovementWarning
