import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from telegram_bot.client import client_router


load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_router(client_router)
