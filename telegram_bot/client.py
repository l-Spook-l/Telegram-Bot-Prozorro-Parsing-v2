from aiogram import types, Router, F
from aiogram.filters import CommandStart

client_router = Router()


@client_router.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer("Вітаю, оберіть, що потрібно зробити")
