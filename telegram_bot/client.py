import re
from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter, or_f
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from .client_buttons.reply_buttons import action_menu_markup, skip_cancel_markup
from .client_buttons.inline_buttons import get_callback_btns
from common.validations_options import status_data, procurement_type_data, regions_data
from data_base.operations import orm_add_data, orm_get_data, orm_delete_data, orm_get_one_data, orm_update_one_data

client_router = Router()


class TenderFilterSetup(StatesGroup):
    DK021_2015 = State()
    Status = State()
    Procurement_type = State()
    Region = State()
    Dispatch_time = State()
    Email = State()

    update_tender_filter = None

    texts = {
        "TenderFilterSetup:DK021_2015": "Введіть код ДК021:2015 знову",
        "TenderFilterSetup:Status": "Введіть статус знову",
        "TenderFilterSetup:Procurement_type": "Введіть вид закупівлі знову",
        "TenderFilterSetup:Region": "Введіть регіон знову",
        "TenderFilterSetup:Dispatch_time": "Введіть час відправлення знову",
    }


@client_router.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer("Вітаю, оберіть, що потрібно зробити", reply_markup=action_menu_markup)


@client_router.message(Command("help"))
@client_router.message(F.text.casefold() == "довідка")
async def help_user(message: types.Message):
    await message.answer(
        "Інструкція використання бота."
        "\nУ нашому боті ви можете налаштувати параметри потрібних вам тендерів та отримувати їх на електронну пошту. "
        "\nНаразі реалізований пошук тендерів за чотирма параметрами: Статус, Вид закупівлі, ДК021:2015 та Регіон. "
        "\nДля параметру Регіон можна вказати лише одне значення у одному запиті (це обмеження Prozorro), "
        "а для решти параметрів можна вказувати кілька значень, розділивши їх комами."
        "\n"
        "\n       <b><u>Приклад фільтру для тендерів</u></b>"
        "\nДК021:2015: 09300000-2"
        "\nСтатус: період уточнень, прекваліфікація"
        "\nВид закупівлі: спрощена закупівля"
        "\nРегіон: київська область"
        "\nЧас відправлення: 18:08"
        "\nПошта: ваша пошта"
        "\nТакож, якщо вам щось не потрібно, ви можете натиснути кнопку - пропустити."
        "\nКонтакти: uaspookua@gmail.com",
        parse_mode="HTML")


@client_router.message(StateFilter(None), F.text == "Додати новий фільтр")
async def create_new_filter(message: types.Message, state: FSMContext):
    await message.answer('Введіть код ДК021:2015', reply_markup=skip_cancel_markup)
    await state.set_state(TenderFilterSetup.DK021_2015)


@client_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def update_filter(callback_query: types.CallbackQuery, state: FSMContext):
    tender_filter_id = int(callback_query.data.split("_")[-1])
    get_data = await orm_get_one_data(tender_filter_id)
    TenderFilterSetup.update_tender_filter = get_data
    await callback_query.answer()
    await callback_query.message.answer("Якщо вам не потрібно змінити пункт то введіть крапку - .")
    await callback_query.message.answer(
        'Введіть код ДК021:2015', reply_markup=skip_cancel_markup
    )
    await state.set_state(TenderFilterSetup.DK021_2015)


@client_router.message(StateFilter("*"), Command("Відміна"))
@client_router.message(StateFilter("*"), F.text.casefold() == "відміна")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    elif TenderFilterSetup.update_tender_filter:
        TenderFilterSetup.update_tender_filter = None
        await message.reply('Змінення фільтру скасовано', reply_markup=action_menu_markup)
    else:
        await message.reply('Додавання нового запиту скасовано', reply_markup=action_menu_markup)
    await state.clear()


@client_router.message(StateFilter("*"), Command("назад"))
@client_router.message(StateFilter("*"), F.text.casefold() == "назад")
async def back_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == TenderFilterSetup.DK021_2015:
        await message.answer("Це перший пункт, що потрібно заповнити, введіть код або натисніть кнопку відміна")
        return
    previous = None
    for step in TenderFilterSetup.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ви повернулись до попереднього шагу. \n{TenderFilterSetup.texts[previous.state]}")
        previous = step


@client_router.message(TenderFilterSetup.DK021_2015, or_f(F.text, F.text == "."))
async def DK021_2015(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(DK021_2015=TenderFilterSetup.update_tender_filter.DK021_2015)
        await message.answer('Введіть статус')
        await state.set_state(TenderFilterSetup.Status)
    else:
        """Pattern for checking the DK021_2015 code"""
        pattern = r'^\d{8}-\d{1,3}$'
        DK021_2015_input = [code.strip() for code in message.text.lower().split(',')]
        valid_code = [code for code in DK021_2015_input if re.match(pattern, code) or code == 'пропустити']
        if valid_code:
            await state.update_data(user=message.from_user.id)
            await state.update_data(DK021_2015=', '.join(valid_code))
            await message.answer('Введіть статус')
            await state.set_state(TenderFilterSetup.Status)
        else:
            await message.answer('Не вірний код, введіть ще раз')
            await message.answer('Введіть код ДК021:2015')


@client_router.message(TenderFilterSetup.Status, or_f(F.text, F.text == "."))
async def status(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(Status=TenderFilterSetup.update_tender_filter.Status)
        await message.answer('Введіть вид закупівлі')
        await state.set_state(TenderFilterSetup.Procurement_type)
    else:
        status_input = message.text.lower().split(', ')
        valid_statuses = [status for status in status_input if status in status_data or status == 'пропустити']
        if valid_statuses:
            await state.update_data(Status=', '.join(valid_statuses))
            await message.answer('Введіть вид закупівлі')
            await state.set_state(TenderFilterSetup.Procurement_type)
        else:
            await message.answer('Такого статусу немає, введіть ще раз')
            await message.answer('Введіть статус')


@client_router.message(TenderFilterSetup.Procurement_type, or_f(F.text, F.text == "."))
async def procurement_type(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(Status=TenderFilterSetup.update_tender_filter.Procurement_type)
        await message.answer('Оберіть потрібний регіон')
        await state.set_state(TenderFilterSetup.Region)
    else:
        procurement_type_input = message.text.lower().split(', ')
        valid_procurement_types = [procurement_type for procurement_type in procurement_type_input if
                                   procurement_type in procurement_type_data or procurement_type == 'пропустити']
        if valid_procurement_types:
            await state.update_data(Procurement_type=', '.join(valid_procurement_types))
            await message.answer('Оберіть потрібний регіон')
            await state.set_state(TenderFilterSetup.Region)
        else:
            await message.answer('Такого виду закупівлі немає, введіть ще раз')
            await message.answer('Введіть вид закупівлі')


@client_router.message(TenderFilterSetup.Region, or_f(F.text, F.text == "."))
async def region(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(Status=TenderFilterSetup.update_tender_filter.Region)
        await message.answer('Введіть час відправлення повідомлення на електронну пошту')
        await state.set_state(TenderFilterSetup.Dispatch_time)
    else:
        region_input = message.text.lower().split(', ')
        valid_region = [region for region in region_input if region in regions_data or region == 'пропустити']
        if valid_region:
            await state.update_data(Region=', '.join(valid_region))
            await message.answer('Введіть час відправлення повідомлення на електронну пошту')
            await state.set_state(TenderFilterSetup.Dispatch_time)
        else:
            await message.answer('Такого регіону немає, введіть ще раз')
            await message.answer('Оберіть потрібний регіон')


@client_router.message(TenderFilterSetup.Dispatch_time, or_f(F.text, F.text == "."))
async def dispatch_time(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(Status=TenderFilterSetup.update_tender_filter.Dispatch_time)
    else:
        """Removing all characters except digits."""
        cleaned_time = re.sub(r'\D', '', message.text)
        """Adding a colon ':' after the first two digits."""
        formatted_time = cleaned_time[:2] + ":" + cleaned_time[2:]
        await state.update_data(Dispatch_time=formatted_time)
    await message.answer('Введіть адрес електронної пошти')
    await state.set_state(TenderFilterSetup.Email)


@client_router.message(TenderFilterSetup.Email, or_f(F.text, F.text == "."))
async def email(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(Status=TenderFilterSetup.update_tender_filter.Email)
    else:
        await state.update_data(Email=message.text.lower())

    data = await state.get_data()

    if TenderFilterSetup.update_tender_filter:
        success = await orm_update_one_data(TenderFilterSetup.update_tender_filter.id, data)
    else:
        success = await orm_add_data(data)

    if success:
        if TenderFilterSetup.update_tender_filter:
            await message.answer('Фільтр успішно змінено', reply_markup=action_menu_markup)
        else:
            await message.answer('Новий фільтру успішно додано', reply_markup=action_menu_markup)
    else:
        await message.answer('Виникла внутрішня помилка, будь ласка спробуйте пізніше',
                             reply_markup=action_menu_markup)
    await state.clear()


@client_router.message(F.text.casefold() == "ваші фільтри")
async def list_filters(message: types.Message):
    await message.reply('Список ваших фільтри')
    get_data = await orm_get_data(message)
    if get_data:
        for user_settings in get_data:
            await message.answer(
                f'ДК021:2015: {user_settings.DK021_2015}\nСтатус: {user_settings.Status}\n'
                f'Вид закупівлі: {user_settings.Procurement_type}\nРегіон: {user_settings.Region}'
                f'\nЧас відправки: {user_settings.Dispatch_time}\nПошта: {user_settings.Email}',
                reply_markup=get_callback_btns(btns={
                    "Видалити": f"delete_{user_settings.id}",
                    "Змінити": f"change_{user_settings.id}",
                })
            )
    elif len(get_data) == 0:
        await message.answer('У вас нема створених фільтрів.',
                             reply_markup=action_menu_markup)
    else:
        await message.answer('Виникла внутрішня помилка, будь ласка спробуйте пізніше',
                             reply_markup=action_menu_markup)


@client_router.callback_query(F.data.startswith("delete_"))
async def delete_filter(callback_query: types.CallbackQuery):
    tender_filter_id = int(callback_query.data.split("_")[-1])
    success = await orm_delete_data(tender_filter_id)
    if success:
        await callback_query.answer(text='Фільтр успішно видалено', show_alert=True)
        await callback_query.message.answer("Фільтр видалено")
    else:
        await callback_query.answer(text='Виникла внутрішня помилка, будь ласка спробуйте пізніше', show_alert=True)

