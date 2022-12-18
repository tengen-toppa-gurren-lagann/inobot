import sqlite3
import pytest

from unittest.mock import AsyncMock

from aiogram.types import ReplyKeyboardRemove

from handlers import db_name, start, show_set, show_help, get_list
from keyboards import keyboard


@pytest.mark.asyncio
async def test_start():
    message = AsyncMock()
    message.from_user.id = 123
    message.from_user.username = 'Pupkin'
    # Проверим 2 случая вызова start()
    # 1-й: пользователя заведомо нет в БД
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute("""DROP TABLE IF EXISTS list""")
    connect.commit()
    await start(message)
    # Проверим, что пользователь добавлен
    cursor.execute(f"SELECT id FROM list WHERE id = {message.from_user.id}")
    assert cursor.fetchone() is not None
    # Проверим, что бот выдает правильное сообщение в ответ
    message.answer.assert_called_with('Welcome to the club, buddy\nType /help for bot info')
    # 2-й: пользователь уже есть в БД
    # Проверим, что количество записей в БД не изменится
    cursor.execute(f"SELECT COUNT(*) from list")
    count = cursor.fetchone()
    await start(message)
    cursor.execute(f"SELECT COUNT(*) from list")
    assert cursor.fetchone() == count
    # Проверим, что бот выдает правильное сообщение в ответ
    message.answer.assert_called_with('Ты уже в книжечке')
    connect.commit()


@pytest.mark.asyncio
async def test_show_set():
    message = AsyncMock()
    await show_set(message)
    message.answer.assert_called_with('Оставь надежду всяк сюда входящий.', reply_markup=keyboard)


@pytest.mark.asyncio
async def test_show_help():
    message = AsyncMock()
    await show_help(message)
    message.answer.assert_called_with('Телеграм-бот для чата, поддерживающий классовое неравенство.\n'
                                      'Список команд:\n/Госуслуги - меню бота\n/Хто_я - регалии и статус пользователя')


@pytest.mark.asyncio
async def test_warn_list():
    await test_start()  # Создали БД с одним пользователем - не иноагентом
    # Заведем ещё три пользователя в тестовую БД, два из которых - иноагенты
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    user1 = [666, "Admin", "1", "1"]
    cursor.execute("INSERT INTO list VALUES(?, ?, ?, ?);", user1)
    user2 = [1, "NotIno", "0", "0"]
    cursor.execute("INSERT INTO list VALUES(?, ?, ?, ?);", user2)
    user3 = [2, "Ino", "1", "0"]
    cursor.execute("INSERT INTO list VALUES(?, ?, ?, ?);", user3)
    connect.commit()
    message = AsyncMock()
    await get_list(message)
    message.answer.assert_called_with("Admin, Ino", reply_markup=ReplyKeyboardRemove())


"""
@pytest.mark.asyncio
async def test_add_ino():
    # Добавим в БД админа
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    user = [666, "admin", "0", "1"]
    cursor.execute("INSERT INTO list VALUES(?, ?, ?, ?);", user)
    connect.commit()
    # Добавим иноагента
    message = AsyncMock()
    message.from_user.id = 666
    message.chat.id = ?
    await add_ino(message)
    message.answer.assert_called_with('Кто на этот раз?')
    message.text = "@Pupkin"
    await naming(message, Control.ino_name)
    message.answer.assert_called_with(f'Решение вынесено.\nОтныне {name} признаётся иноагентом.')
"""
