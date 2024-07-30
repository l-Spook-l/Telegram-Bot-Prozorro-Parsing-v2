import asyncio
from config import dp, bot


async def start_bot():
    print('Bot online!')
    await dp.start_polling(bot)


async def main():
    tasks = [start_bot()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")


