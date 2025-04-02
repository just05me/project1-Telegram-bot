import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F

# Подключение бота
HellYeahItMybot = Bot(token="Telegra-bot token")
dp = Dispatcher()

# Функция создающая базу данных
def setup_database():
    conn = sqlite3.connect("my_notes.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, user_id INTEGER, note_text TEXT)")
    conn.commit()
    return conn, cursor

# Функция для сохранения данных
def save_note(cursor, conn, user_id, note_text):
    cursor.execute("INSERT INTO notes (user_id, note_text) VALUES (?, ?)", (user_id, note_text))
    conn.commit()

# Функция для показывающая созраненные данные
def get_notes(cursor, user_id):
    cursor.execute("SELECT id, note_text FROM notes WHERE user_id = ?", (user_id,))
    return cursor.fetchall()

# Функция для удаления данных
def delete_note(cursor, conn, note_id, user_id):
    cursor.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id))
    conn.commit()

# Создаём базу данных
connection, cursor = setup_database()

# Команда /start
@dp.message(F.text.startswith("/start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот для заметок. Пиши:\n/add текст - добавить заметку\n/list - показать все заметки\n/delete номер - удалить заметку")

# Команда /add
@dp.message(F.text.startswith("/add"))
async def add_note_command(message: types.Message):
    note_text = message.text.replace("/add ", "")
    user_id = message.from_user.id
    save_note(cursor, connection, user_id, note_text)
    await message.answer("Заметка сохранена!")

# Команда /list
@dp.message(F.text.startswith("/list"))
async def list_notes_command(message: types.Message):
    user_id = message.from_user.id
    notes = get_notes(cursor, user_id)
    if notes:
        text = "Вот твои заметки:\n"
        for note in notes:
            text += f"Номер: {note[0]} - {note[1]}\n"
        await message.answer(text)
    else:
        await message.answer("У тебя нет заметок!")

# Команда /delete
@dp.message(F.text.startswith("/delete"))
async def delete_note_command(message: types.Message):
    note_id = message.text.replace("/delete ", "")
    user_id = message.from_user.id
    delete_note(cursor, connection, note_id, user_id)
    await message.answer("Заметка удалена!")

# Запуск бота
async def main():
    await dp.start_polling(HellYeahItMybot)

if __name__ == '__main__':
    asyncio.run(main())
