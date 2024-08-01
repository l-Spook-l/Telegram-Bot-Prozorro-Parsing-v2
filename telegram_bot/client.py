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
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from .client_buttons import action_menu_markup, skip_cancel_markup
from common.options import status_data, procurement_type_data, regions_data
from data_base.operations import sql_add_data, sql_read, sql_delete_data, sql_read_for_del

client_router = Router()


class AddTenders(StatesGroup):
    DK021_2015 = State()
    Status = State()
    Procurement_type = State()
    Region = State()
    Dispatch_time = State()
    Email = State()

    texts = {
        "AddTenders:DK021_2015": "Введіть код ДК021:2015 знову",
        "AddTenders:Status": "Введіть статус знову",
        "AddTenders:Procurement_type": "Введіть  вид закупівлі знову",
        "AddTenders:Region": "Введіть регіон знову",
        "AddTenders:Dispatch_time": "Введіть час відправлення знову",
    }


@client_router.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer("Вітаю, оберіть, що потрібно зробити", reply_markup=action_menu_markup)


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
        "\nЧас відправлення: 18:08"
        "\nПошта: ваша пошта"
        "\nТакож, якщо вам щось не потрібно, ви можете натиснути кнопку - пропустити."
        "\nКонтакти: uaspookua@gmail.com", )


@client_router.message(StateFilter(None), F.text == "Додати запит")
async def create_new_request(message: types.Message, state: FSMContext):
    await message.answer('Введіть код ДК021:2015', reply_markup=skip_cancel_markup)
    await state.set_state(AddTenders.DK021_2015)


@client_router.message(StateFilter("*"), Command("Відміна"))
@client_router.message(StateFilter("*"), F.text.casefold() == "відміна")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply('Додавання нового запиту скасовано', reply_markup=action_menu_markup)


@client_router.message(StateFilter("*"), Command("назад"))
@client_router.message(StateFilter("*"), F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == AddTenders.DK021_2015:
        await message.answer("Це перший пункт, що потрібно заповнити, введіть код або натисніть кнопку відміна")

    previous = None
    for step in AddTenders.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ви повернулись до попереднього шагу. \n{AddTenders.texts[previous.state]}")
        previous = step


@client_router.message(AddTenders.DK021_2015, F.text)
async def DK021_2015(message: types.Message, state: FSMContext):
    # Pattern for checking the DK021_2015 code
    pattern = r'^\d{8}-\d{1,3}$'
    DK021_2015_input = [code.strip() for code in message.text.lower().split(',')]
    valid_code = [code for code in DK021_2015_input if re.match(pattern, code) or code == 'пропустити']
    if valid_code:
        await state.update_data(user=message.from_user.id)
        await state.update_data(DK021_2015=valid_code)
        await message.answer('Введіть статус')
        await state.set_state(AddTenders.Status)
    else:
        await message.answer('Не вірний код, введіть ще раз')
        await message.answer('Введіть код ДК021:2015')


@client_router.message(AddTenders.Status, F.text)
async def status(message: types.Message, state: FSMContext):
    status_input = message.text.lower().split(', ')
    valid_statuses = [status for status in status_input if status in status_data or status == 'пропустити']
    if valid_statuses:
        await state.update_data(Status=valid_statuses)
        await message.answer('Введіть вид закупівлі')
        await state.set_state(AddTenders.Procurement_type)
    else:
        await message.answer('Такого статусу немає, введіть ще раз')
        await message.answer('Введіть статус')


@client_router.message(AddTenders.Procurement_type, F.text)
async def procurement_type(message: types.Message, state: FSMContext):
    procurement_type_input = message.text.lower().split(', ')

    valid_procurement_types = [procurement_type for procurement_type in procurement_type_input if
                               procurement_type in procurement_type_data or procurement_type == 'пропустити']
    if valid_procurement_types:
        await state.update_data(Procurement_type=valid_procurement_types)
        await message.answer('Оберіть потрібний регіон')
        await state.set_state(AddTenders.Region)
    else:
        await message.answer('Такого виду закупівлі немає, введіть ще раз')
        await message.answer('Введіть вид закупівлі')


@client_router.message(AddTenders.Region, F.text)
async def region(message: types.Message, state: FSMContext):
    region_input = message.text.lower().split(', ')
    valid_region = [region for region in region_input if region in regions_data or region == 'пропустити']
    if valid_region:
        await state.update_data(Region=valid_region)
        await message.answer('Введіть час відправлення повідомлення на електронну пошту')
        await state.set_state(AddTenders.Dispatch_time)
    else:
        await message.answer('Такого регіону немає, введіть ще раз')
        await message.answer('Оберіть потрібний регіон')


@client_router.message(AddTenders.Dispatch_time, F.text)
async def dispatch_time(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    # Removing all characters except digits.
    cleaned_time = re.sub(r'\D', '', message.text)
    # Adding a colon ':' after the first two digits.
    formatted_time = cleaned_time[:2] + ":" + cleaned_time[2:]
    await state.update_data(Region=formatted_time)
    await message.answer('Введіть адрес електронної пошти')
    await state.set_state(AddTenders.Email)


@client_router.message(AddTenders.Email, F.text)
async def email(message: types.Message, state: FSMContext):
    await state.update_data(Email=message.text.lower())
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()
