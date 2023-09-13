from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu():
    add = KeyboardButton(text='Добавить сотрудника')
    remove = KeyboardButton(text='Удалить сотрудника')
    edit = KeyboardButton(text='Редактировать сотрудника')
    find = KeyboardButton(text='Поиск сотрудника')
    buttons = [[add], [remove], [edit], [find]]
    kb = ReplyKeyboardMarkup(keyboard=buttons)
    return kb

def generate_users_keyboard(users):
    buttons = []
    for user in users:
        text = f"[{user['id']}] {user['first_name']} {user['last_name']}"
        button = [KeyboardButton(text=text)]
        buttons.append(button)
    kb = ReplyKeyboardMarkup(keyboard=buttons)
    return kb
