from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


action_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ваші запити'),
        ],
        [
            KeyboardButton(text='Додати запит'),
            KeyboardButton(text='Видалити запит'),
        ],
        [
            KeyboardButton(text='Довідка'),
        ]
    ],
    resize_keyboard=True,
)

