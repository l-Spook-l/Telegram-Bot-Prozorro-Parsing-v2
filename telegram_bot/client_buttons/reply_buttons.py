from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


action_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ваші запити'),
            KeyboardButton(text='Додати запит'),
        ],
        [
            KeyboardButton(text='Довідка'),
        ]
    ],
    resize_keyboard=True
)

skip_cancel_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Пропустити'),
        ],
        [
            KeyboardButton(text='Відміна'),
            KeyboardButton(text='Назад'),
        ],
    ],
    resize_keyboard=True
)
