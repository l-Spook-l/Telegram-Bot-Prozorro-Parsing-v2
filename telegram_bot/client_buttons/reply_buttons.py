from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

action_menu_markup = ReplyKeyboardBuilder()
action_menu_markup.add(
    KeyboardButton(text='Ваші фільтри'),
    KeyboardButton(text='Додати новий фільтр'),
    KeyboardButton(text='Довідка'),
)
action_menu_markup.adjust(2, 1)

skip_cancel_markup = ReplyKeyboardBuilder()
skip_cancel_markup.add(
    KeyboardButton(text='Пропустити'),
    KeyboardButton(text='Відміна'),
    KeyboardButton(text='Назад'),
)
skip_cancel_markup.adjust(1, 2)

skip_cancel_markup_update = ReplyKeyboardBuilder()
skip_cancel_markup_update.add(
    KeyboardButton(text='Пропустити'),
    KeyboardButton(text='Не змінювати пункт'),
    KeyboardButton(text='Відміна'),
    KeyboardButton(text='Назад'),
)
skip_cancel_markup_update.adjust(2, 2)
