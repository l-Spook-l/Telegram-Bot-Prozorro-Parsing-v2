from aiogram import types
from aiogram.fsm.context import FSMContext
from data_base.operations import orm_add_data, orm_update_one_data
from telegram_bot.client_buttons.reply_buttons import action_menu_markup


async def get_data_tender(data) -> list | bool:
    """Implemented data preparation for parsing and subsequent sending to the user via email"""
    data_list = []
    try:
        for user_tender in data:
            tender = user_tender[0]
            data_list.append({
                'id': tender.id,
                'user': tender.user,
                'ДК021:2015': tender.DK021_2015,
                'Статус': tender.Status,
                'Вид закупівлі': tender.Procurement_type,
                'Регіон': tender.Region,
                'Час відправки': tender.Dispatch_time,
                'Пошта': tender.Email,
            })
        return data_list
    except Exception as error:
        print(f"Error occurred while get data: {error}")
        return False


async def update_filter_or_add_data(state: FSMContext, message: types.Message) -> None:
    from telegram_bot.client import TenderFilterSetup

    data = await state.get_data()

    if TenderFilterSetup.update_tender_filter:
        success = await orm_update_one_data(TenderFilterSetup.update_tender_filter.id, data)
        response_message = \
            ("<b><u>Фільтр успішно змінено</u></b> "
             "\nБудь ласка переконайтися, що усі пункти вірні, натиснувши кнопку - 'Ваші запити'") \
                if success else "Виникла внутрішня помилка, будь ласка спробуйте пізніше"
    else:
        success = await orm_add_data(data)
        response_message = \
            ("<b><u>Новий фільтру успішно додано</u></b>"
             "\n Будь ласка переконайтися, що усі пункти вірні, натиснувши кнопку - 'Ваші запити'") \
                if success else "Виникла внутрішня помилка, будь ласка спробуйте пізніше"

    await message.answer(response_message, reply_markup=action_menu_markup.as_markup(resize_keyboard=True),
                         parse_mode="HTML")
    await state.clear()


async def send_error_message(user_id: str, error_message: str) -> None:
    from config import bot
    await bot.send_message(int(user_id), f"An error occurred: {error_message}")
