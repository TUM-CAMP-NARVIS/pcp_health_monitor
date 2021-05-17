import asyncio
import logging

import schemata as schema


class MonitorService(object):

    brightness_lock = asyncio.Lock()

    # access shared state
    brightness_events = []
    fps_events = []

    async def monitor(self, socket):
        while True:
            msg = await socket.recv()
            print(schema.events.ApplicationEvent.from_bytes(msg))
            async with self.brightness_lock:
                # save brightness events
                pass

    async def process_events(self):
        while True:
            async with self.brightness_lock:
                if len(self.brightness_events) == 0:
                    logging.info("No events to process...")

            await asyncio.sleep(0.3)
