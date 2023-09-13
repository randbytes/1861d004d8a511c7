from db import Database
def serialize_key(key):
    if key == "Имя":
        return "first_name"
    if key == "Фамилия":
        return "last_name"
    if key == "Отчество":
        return "surname"
    if key == "Должность":
        return "position"
    if key == "Проект":
        return "project"
    if key == "Аватар":
        return "avatar"
    return ""

def deserialize_key(key):
    if key == "first_name":
        return "Имя"
    if key == "last_name":
        return "Фамилия"
    if key == "surname":
        return "Отчество"
    if key == "position":
        return "Должность"
    if key == "project":
        return "Проект"
    if key == "avatar":
        return "Аватар"
    return ""

class Service:
    def __init__(self, con, chat_id) -> None:
        self.con = con
        self.chat_id = chat_id
        self.db = Database(self.con)
        self.__all_columns = ["id", "first_name", "last_name", "surname", "position", "project", "avatar"]
        pass
    def parse_user_from_form(self, text: str):
        insert_obj = {
        }
        lines = text.splitlines()
        for line in lines:
            key, value = line.split(":")
            key, value = serialize_key(key.strip()), value.strip()
            insert_obj[key] = value
        insert_obj["first_name_last_name"] = f"{insert_obj['first_name']}{insert_obj['last_name']}".upper()
        insert_obj["authorId"] = self.chat_id
        return insert_obj
    
    def add_employee(self, text: str):
        try:
            required_keys = ["first_name", "last_name", "surname", "position", "project"]
            insert_obj = self.parse_user_from_form(text)
            if all(key in insert_obj for key in required_keys):
                self.db.insert("users", insert_obj)
                return f"Сотрудник {insert_obj['first_name']} {insert_obj['last_name']} добавлен"
            return False
        except Exception as e:
            return False

    def get_all_employees(self):
        users = self.db.fetch("users", self.chat_id, self.__all_columns)
        return users

    def remove_employee(self, _id):
        users = self.db.delete("users", self.chat_id, _id)
        return users

    def edit_employee(self, id, text):
        insert_obj = {
        }
        lines = text.splitlines()
        for line in lines:
            key, value = line.split(":")
            key, value = serialize_key(key.strip()), value.strip()
            insert_obj[key] = value
        insert_obj["first_name_last_name"] = f"{insert_obj['first_name']}{insert_obj['last_name']}".upper()
        self.db.update("users", id, self.chat_id, insert_obj)
        return f"Данные обновлены"

    def find_employee(self, text):
        result = self.db.find("users", self.chat_id, "first_name_last_name", f"%{text.upper()}%", self.__all_columns)
        return result
