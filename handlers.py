import sqlite3

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text, Command

from keyboards import keyboard

from main import bot, dp
from config import chat_id


async def send_hello(dp):
    await bot.send_message(chat_id=chat_id, text='ПРИВА))))')


@dp.message_handler(Command('start'))
async def start(message):
    connect = sqlite3.connect('db.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS list(
        id       INTEGER,
        name     TEXT,
        regalias INTEGER,
        statuses INTEGER
    )""")

    connect.commit()

    human_id = message.from_user.id
    user = message.from_user.username
    cursor.execute(f"SELECT id FROM list WHERE id = {human_id}")
    data = cursor.fetchone()
    if data is None:
        user_id = [human_id, user, "0", "0"]
        cursor.execute("INSERT INTO list VALUES(?, ?, ?, ?);", user_id)
        connect.commit()
    else:
        text = 'Ты уже в книжечке'
        await message.answer(text=text)


@dp.message_handler(Command('Госуслуги'))
async def show_set(message: Message):
    await message.answer('Оставь надежду всяк сюда входящий', reply_markup=keyboard)


@dp.message_handler(Command('Хто_я'))
async def show_who(message: Message):
    connect = sqlite3.connect('db.db')
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
    await message.answer(text=text)


# @dp.message_handler(Text(equals=['Список иноагентов', 'Оповестить', 'Добавить иноагента', 'Амнистировать иноагента']))

@dp.message_handler(Text(equals=['Список иноагентов']))
async def get_list(message: Message):
    text = ''
    connect = sqlite3.connect('db.db')
    cursor = connect.cursor()
    human_regalia = '1'
    cursor.execute(f"SELECT * FROM list WHERE regalias = {human_regalia}")
    data = cursor.fetchall()
    if data is not None:
        for row in data:
            # text = ''.join(row[1])
            text += '@' + row[1] + ', '
    text = text[:-2]
    await message.answer(text=text)


@dp.message_handler()
async def send_answer(message: Message):
    connect = sqlite3.connect('db.db')
    cursor = connect.cursor()
    human_id = message.from_user.id
    human_regalia = '1'
    cursor.execute(f"SELECT id FROM list WHERE id = {human_id} AND regalias = {human_regalia}")
    data = cursor.fetchone()
    if data is not None:
        text = 'ДАННОЕ СООБЩЕНИЕ (МАТЕРИАЛ) СОЗДАНО И (ИЛИ) РАСПРОСТРАНЕНО ИНОСТРАННЫМ СРЕДСТВОМ МАССОВОЙ ИНФОРМАЦИИ, ' \
               'ВЫПОЛНЯЮЩИМ ФУНКЦИИ ИНОСТРАННОГО АГЕНТА, И (ИЛИ) РОССИЙСКИМ ЮРИДИЧЕСКИМ ЛИЦОМ, ВЫПОЛНЯЮЩИМ ФУНКЦИИ ' \
               'ИНОСТРАННОГО АГЕНТА. '
        await message.answer(text=text)
