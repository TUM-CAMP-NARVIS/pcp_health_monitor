import os
import json
import logging
import asyncio
from dotenv import load_dotenv
from pathlib import Path

from aiogram import Bot, executor, Dispatcher, types

logger = logging.getLogger(__name__)

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
# Configure logger
bot = Bot(token=API_TOKEN)
# not nice to have this defined on load..
# in future we can replace the decorators
# and register the callbacks manually..
dp = Dispatcher(bot)

class SimpleCache(object):
    users = []
    path = None
    def __init__(self, path):
        if os.path.exists(path):
            logger.info(f"Loading storage dir: {storage_path}")
            with open(path) as infile:
                try:
                    data = json.load(infile)
                except json.decoder.JSONDecodeError:
                    logger.warning("Cache invalid.. removing")
                    os.remove(path)
                    data = []
                logger.info(f"loaded cache for {len(data)} users: {data}")
            self.users = data
        self.path = path

    def add_user(self, user_id):
        if user_id not in self.users:
            self.users.append(user_id)
            self.flush()

    def remove_user(self, user_id):
        if user_id in self.users:
            self.users.remove(user_id)
            self.flush()

    def flush(self):
        with open(self.path, "w") as outfile:
            logger.info(f"writing cache data: {self.users}")
            json.dump(self.users, outfile, indent=4)

storage_path = Path.cwd() / "telegram_user_ids.json"
cache = SimpleCache(storage_path)

@dp.message_handler(commands=['help'])
@dp.message_handler(lambda msg: msg.text.lower() == 'help')
async def help_handler(message: types.Message):
    await bot.send_message(message.from_user.id,
        """ATLAS health monitoring bot..
            * register with /register
            * deregister with /deregister
        """)
    cache.remove_user(message.from_user.id)

@dp.message_handler(commands=['register'])
@dp.message_handler(lambda msg: msg.text.lower() == 'register')
async def register(message: types.Message):
    """
    This handler will be called when user sends `/register` or command
    """
    await message.reply("""Registered to recieve ATLAS health monitoring notifications..\n
                        Type 'help' for list of available commands.""")
    cache.add_user(message.from_user.id)

@dp.message_handler(commands=['deregister'])
@dp.message_handler(lambda msg: msg.text.lower() == 'deregister')
async def cancel_handler(message: types.Message):
    await bot.send_message(message.from_user.id, 'Removed ATLAS health monitoring alerts..')
    cache.remove_user(message.from_user.id)

@dp.message_handler()
async def echo(message: types.Message, indent=4): await message.answer(message.text, disable_notification=True)

async def _tick():
    while True:
        await asyncio.sleep(5)
        logger.info("Tick...")
        for user_id in cache.users:
            logger.info(f"User registered: {user_id}")
            await bot.send_message(user_id, "tick..", disable_notification=True)

async def message_all_users(text, disable_notifications=True):
    """Send telegram message to all registered users"""
    for user_id in cache.users:
        await bot.send_message(user_id, text, disable_notification=disable_notifications)

async def initialize_telegram_bot():
    """Starts the telegram bot..
    * register with /register
    * deregister with /cancel
    """
    # hack to start executor so it's not synchronous
    exc = executor.Executor(dp, skip_updates=True)
    exc.freeze = True
    await exc._startup_polling()
    loop = asyncio.get_event_loop()
    logger.info("Start aiogram polling..")
    loop.create_task(dp.start_polling())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(initialize_telegram_bot())
    asyncio.run(_tick())
