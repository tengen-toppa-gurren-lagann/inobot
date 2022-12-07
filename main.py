import asyncio

from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN

loop = asyncio.new_event_loop()
storage = MemoryStorage()
bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp)
