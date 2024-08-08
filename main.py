import asyncio
import datetime
from aiogram import types
from config import dp, bot
from data_base.operations import orm_read_time
from common.bot_cmds_list import private
from common.utils import get_data_send_email, get_data_tender


async def check_update_database() -> None:
    print('Start check update database')
    time_correction = datetime.timedelta(seconds=0)
    while True:
        await asyncio.sleep(60 - time_correction.total_seconds())
        now = datetime.datetime.now()
        formatted_time = now.strftime("%H:%M")
        print('=================Time now: ', datetime.datetime.now(), '===============================')
        check_data = await orm_read_time(formatted_time)
        """If there's something during the time check"""
        if check_data:
            data = await get_data_tender(check_data)
            tasks = [get_data_send_email([data[i]]) for i in range(len(data))]
            await asyncio.gather(*tasks)
        time_correction = datetime.datetime.now() - now
        print(f'###################### Uncertainty - {time_correction.total_seconds()} ###########################')


async def start_bot() -> None:
    print('Bot online!')
    await bot.delete_webhook(drop_pending_updates=True)  # для сброса накопившихся обновлений
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())  # если надо удалить меню команд
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)  # урок #3 ограничить типы обновлений !!!!!!!!!!!!!!!


async def main() -> None:
    tasks = [check_update_database(), start_bot()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
