import sqlite3

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from src.keyboards import keyboard
from src.main import bot, dp

db_name = "db.db"


class Control(StatesGroup):
    ino_name = State()
    not_ino = State()


@dp.message_handler(Command('start'))
async def start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS list(
        id       INTEGER,
        name     TEXT,
        regalias INTEGER,
        statuses INTEGER
    )""")
    connect.commit()
    cursor.execute(f"SELECT id FROM list WHERE id = {user_id}")
    data = cursor.fetchone()
    if data is None:
        user = [user_id, user_name, "0", "0"]
        cursor.execute("INSERT INTO list VALUES(?, ?, ?, ?);", user)
        connect.commit()
        text = 'Welcome to the club, buddy\nType /help for bot info'
    else:
        text = 'Ты уже в книжечке'
    await message.answer(text)


@dp.message_handler(Command('Госуслуги'))
async def show_set(message: Message):
    await message.answer('Оставь надежду всяк сюда входящий.', reply_markup=keyboard)


@dp.message_handler(Command('help'))
async def show_help(message: Message):
    text = 'Телеграм-бот для чата, поддерживающий классовое неравенство.\nСписок команд:\n/Госуслуги - меню бота' \
           '\n/Хто_я - регалии и статус пользователя'
    await message.answer(text)


@dp.message_handler(Command('Хто_я'))
async def show_who(message: Message):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    human_id = message.from_user.id
    text = ""
    human_regalia = '1'
    status = '1'
    cursor.execute(f"SELECT id FROM list WHERE regalias = {human_regalia} AND id = {human_id}")
    data1 = cursor.fetchone()
    cursor.execute(f"SELECT id FROM list WHERE statuses = {status} AND id = {human_id}")
    data2 = cursor.fetchone()
    if data1 is not None:
        text += 'Ты клятый иноагент'
    else:
        text += 'Ты хороший подчинённый'
    if data2 is not None:
        text += ' и Верховное зло'
    else:
        text += ' и рядовой рабочий с завода'
    await message.answer(text)


@dp.message_handler(Text(equals=['Добавить иноагента']))
async def add_ino(message: Message):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    human_id = message.from_user.id
    status = '1'
    cursor.execute(f"SELECT id FROM list WHERE statuses = {status} AND id = {human_id}")
    data2 = cursor.fetchone()
    if data2 is not None:
        await bot.send_message(message.chat.id, 'Кто на этот раз?')
        await Control.ino_name.set()


@dp.message_handler(state=Control.ino_name)
async def naming(message: Message, state: FSMContext):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    human_id = message.from_user.id
    status = '1'
    cursor.execute(f"SELECT id FROM list WHERE statuses = {status} AND id = {human_id}")
    data2 = cursor.fetchone()
    if data2 is not None:
        name = message.text.removeprefix("@")
        cursor.execute(f"UPDATE list SET regalias = 1 WHERE name = '{name}'")
        connect.commit()
        await bot.send_message(message.chat.id, f'Решение вынесено.\nОтныне {name} признаётся иноагентом.')
        await state.finish()


@dp.message_handler(Text(equals=['Амнистировать иноагента']))
async def rem_ino(message: Message):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    human_id = message.from_user.id
    status = '1'
    cursor.execute(f"SELECT id FROM list WHERE statuses = {status} AND id = {human_id}")
    data2 = cursor.fetchone()
    if data2 is not None:
        await bot.send_message(message.chat.id, 'Кто помилован?')
        await Control.not_ino.set()


@dp.message_handler(state=Control.not_ino)
async def named(message: Message, state: FSMContext):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    human_id = message.from_user.id
    status = '1'
    cursor.execute(f"SELECT id FROM list WHERE statuses = {status} AND id = {human_id}")
    data2 = cursor.fetchone()
    if data2 is not None:
        name = message.text.removeprefix("@")
        cursor.execute(f"UPDATE list SET regalias = 0 WHERE name = '{name}'")
        connect.commit()
        await bot.send_message(message.chat.id, f'Упс, перепуточки.\nОтныне {name} лишается статуса иноагента.')
        await state.finish()


@dp.message_handler(Text(equals=['Список иноагентов']))
async def get_list(message: Message):
    text = ''
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    human_regalia = '1'
    cursor.execute(f"SELECT * FROM list WHERE regalias = {human_regalia}")
    data = cursor.fetchall()
    if data is not None:
        for row in data:
            text += row[1] + ', '
    text = text[:-2]
    await message.answer(text, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals=['Оповестить']))
async def warn_list(message: Message):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    human_id = message.from_user.id
    text = 'Клятые иноагенты '
    status = '1'
    human_regalia = '1'
    cursor.execute(f"SELECT id FROM list WHERE statuses = {status} AND id = {human_id}")
    data2 = cursor.fetchone()
    cursor.execute(f"SELECT * FROM list WHERE regalias = {human_regalia}")
    data = cursor.fetchall()
    if data2 is not None and data is not None:
        for row in data:
            text += '@' + row[1] + ', '
        text += 'требуется ваше присутствие.'
        await message.answer(text, reply_markup=ReplyKeyboardRemove())


@dp.message_handler()
async def send_answer(message: Message):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    human_id = message.from_user.id
    m = message.message_id
    human_regalia = '1'
    cursor.execute(f"SELECT id FROM list WHERE id = {human_id} AND regalias = {human_regalia}")
    data = cursor.fetchone()
    if data is not None:
        text = 'ДАННОЕ СООБЩЕНИЕ (МАТЕРИАЛ) СОЗДАНО И (ИЛИ) РАСПРОСТРАНЕНО ИНОСТРАННЫМ СРЕДСТВОМ МАССОВОЙ ИНФОРМАЦИИ, '\
               'ВЫПОЛНЯЮЩИМ ФУНКЦИИ ИНОСТРАННОГО АГЕНТА, И (ИЛИ) РОССИЙСКИМ ЮРИДИЧЕСКИМ ЛИЦОМ, ВЫПОЛНЯЮЩИМ ФУНКЦИИ '\
               'ИНОСТРАННОГО АГЕНТА. '
        await bot.send_message(message.chat.id, text, reply_to_message_id=m)
