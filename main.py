import asyncio
import logging
import sys
import sqlite3
import os

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from menu import get_main_menu, generate_users_keyboard
from service import Service, deserialize_key

from dotenv import load_dotenv

# Bot token can be obtained via https://t.me/BotFather
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

con = sqlite3.connect("database.db")

active_commands = {}

# All handlers should be attached to the Router (or Dispatcher)
router = Router()
dp = Dispatcher()

def create_user_card(user):
    text = ""
    for key in user.keys():
        if (key != "id"):
            text += f"{deserialize_key(key)}: {user[key]}\n"
    return text


async def handle_user_command(message, command, stage = None):
    chat_id = message.chat.id
    service = Service(con, chat_id)
    if command == "Add":
        result = service.add_employee(message.text)
        if result:
            await message.answer(result)
        else:
            await message.answer("Данные внесены неверно или не хватает полей")
    if command == "Remove":
        main_menu = get_main_menu()
        _id = message.text.split("]")[0].split("[")[1]
        result = service.remove_employee(_id)
        await message.answer(f"Сотрудник номер {_id} удален", reply_markup=main_menu)
    if command == "Edit":
        if (stage == 2):
            id = active_commands[str(message.chat.id)]["shared"]
            main_menu = get_main_menu()
            result = service.edit_employee(id, message.text)
            await message.answer("Данные обновлены", reply_markup=main_menu)
        else:
            _id = message.text.split("]")[0].split("[")[1]
            text = "Скопируйте форму и введите обновленные данные сотрудника по форме:\nИмя:\nФамилия:\nОтчество:\nДолжность:\nПроект:\nАватар:\n"
            active_commands[str(message.chat.id)]["stage"] = 2
            active_commands[str(message.chat.id)]["shared"] = _id
            await message.answer(text)
            return
    if command == "Find":
        result = service.find_employee(message.text)
        if len(result):
            await message.answer("Сотрудники по вашему запросу")
            for item in result:
                card = create_user_card(item)
                await message.answer(card)
        else:
            await message.answer("Сотрудник(и) не найден")

    active_commands[str(message.chat.id)] = None

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    main_menu = get_main_menu()
    await message.answer(f"Приветствую!\nЯ бот помощник.\nДля взаимодействия со мной я выслал тебе интерактивное меню!\nТы всегда можешь вернуться к нему используя команду /menu", reply_markup=main_menu)

@dp.message(Command("menu"))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/menu` command
    """
    main_menu = get_main_menu()
    await message.answer(f"Вы вернулись в главное меню", reply_markup=main_menu)

@dp.message(F.text == "Добавить сотрудника")
async def add_employee(message: Message) -> None:
    chat_id = str(message.chat.id)
    active_commands[chat_id] = {
        "method":"Add",
        "stage": 1
    }
    text = "Скопируйте форму и введите данные сотрудника соответственно полям:\nИмя:\nФамилия:\nОтчество:\nДолжность:\nПроект:\nАватар:\n"
    await message.answer(text)

@dp.message(F.text == "Удалить сотрудника")
async def remove_employee(message: Message) -> None:
    chat_id = str(message.chat.id)
    service = Service(con, chat_id)
    active_commands[chat_id] = {
        "method":"Remove",
        "stage": 1
    }
    result = service.get_all_employees()
    if len(result):
        keyboard = generate_users_keyboard(result)
        await message.answer(f"Выберите сотрудника в меню", reply_markup=keyboard)
    else:
        await message.answer("Список сотрудников пуст")

@dp.message(F.text == "Редактировать сотрудника")
async def edit_employee(message: Message) -> None:
    chat_id = str(message.chat.id)
    service = Service(con, chat_id)
    active_commands[chat_id] = {
        "method":"Edit",
        "stage": 1
    }
    result = service.get_all_employees()
    if len(result):
        keyboard = generate_users_keyboard(result)
        await message.answer(f"Выберите сотрудника в меню", reply_markup=keyboard)
    else:
        await message.answer("Список сотрудников пуст")

@dp.message(F.text == "Поиск сотрудника")
async def find_employee(message: Message) -> None:
    chat_id = str(message.chat.id)
    active_commands[chat_id] = {
        "method":"Find",
        "stage": 1
    }
    await message.answer(f"Имя и/или фамилия сотрудника")

@dp.message(Command("cancel"))
async def add_employee(message: Message) -> None:
    chat_id = str(message.chat.id)
    active_commands[chat_id] = None
    main_menu = get_main_menu()
    await message.answer(f"Отмена", reply_markup=main_menu)

@dp.message()
async def echo_handler(message: types.Message) -> None:
    chat_id = str(message.chat.id)
    if chat_id in active_commands:
        await handle_user_command(message, active_commands[chat_id]["method"], active_commands[chat_id]["stage"])
    else:
        await message.answer(f"У вас нет активной команды")

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
