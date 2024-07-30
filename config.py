import os
from aiogram import Bot, Dispatcher
from telegram_bot.client import client_router
from dotenv import load_dotenv


load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_router(client_router)
