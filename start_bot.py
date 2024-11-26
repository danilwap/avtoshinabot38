import asyncio
import logging
import sys



from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from db_map import create_table
from aiogram.client.default import DefaultBotProperties
import os
from handlers import user

from dotenv import load_dotenv

load_dotenv()
TOKEN_BOT = os.environ.get("TOKEN_BOT")


async def main():
    create_table()
    dp = Dispatcher()
    dp.include_router(user.router)
    bot = Bot(token=TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
