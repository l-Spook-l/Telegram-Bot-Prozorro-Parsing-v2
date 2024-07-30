# from aiogram import Dispatcher, types
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher import FSMContext
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from Data_base.data_base import sql_add_data, sql_read, sql_delete_data, sql_read_for_del
# from config import bot
# from .client_buttons import action_menu_markup, skip_cancel_markup
# from options import status_data, procurement_type_data, regions_data
import re

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State


client_router = Router()


class FSMClient(StatesGroup):
    DK021_2015 = State()
    Status = State()
    Procurement_type = State()
    Region = State()
    Dispatch_time = State()
    Email = State()


@client_router.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer("Вітаю, оберіть, що потрібно зробити")


@client_router.message(Command("help"))
async def help_user(message: types.Message):
    await message.answer(
        "Інструкція використання бота."
        "\nУ нашому боті ви можете налаштувати параметри потрібних вам тендерів та отримувати їх на електронну пошту. "
        "\nНаразі реалізований пошук тендерів за чотирма параметрами: Статус, Вид закупівлі, ДК021:2015 та Регіон. "
        "\nДля параметру Регіон можна вказати лише одне значення у одному запиті (це обмеження Prozorro), "
        "а для решти параметрів можна вказувати кілька значень, розділивши їх комами."
        "\n                   Приклад запиту:"
        "\nДК021:2015: 09300000-2"
        "\nСтатус: період уточнень, прекваліфікація"
        "\nВид закупівлі: спрощена закупівля"
        "\nРегіон: київська область"
        "\nЧас відправки: 18:08"
        "\nПошта: ваша пошта"
        "\nТакож якщо вам щось не потрібно, ви можете натиснути кнопку - пропустити."
        "\nКонтакти: uaspookua@gmail.com",)


