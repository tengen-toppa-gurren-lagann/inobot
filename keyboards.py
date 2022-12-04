from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData



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