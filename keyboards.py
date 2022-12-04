from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Список иноагентов'),
            KeyboardButton(text='Оповестить')
        ],
        [
            KeyboardButton(text='Добавить иноагента'),
            KeyboardButton(text='Амнистировать иноагента')
        ]
    ],
    resize_keyboard=True
)