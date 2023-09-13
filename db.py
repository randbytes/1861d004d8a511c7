class Database:
    def __init__(self, con) -> None:
        self.con = con

    def fetch(self, table, chat_id, columns):
        cursor = self.con.cursor()
        _columns = ", ".join(columns)
        print(_columns);
        SQL = f"SELECT {_columns} FROM {table} WHERE authorId = ?;"
        cursor.execute(SQL, (chat_id,))
        rows = cursor.fetchall()
        items = []
        for row in rows:
            obj = {}
            for index, column in enumerate(columns):
                obj[column] = row[index]
            items.append(obj)
        cursor.close()
        return items

    def delete(self, table, chat_id, id):
        cursor = self.con.cursor()
        SQL = f"DELETE FROM {table} WHERE authorId = ? AND id = ?"
        cursor.execute(SQL, (chat_id, id, ))
        self.con.commit()
        cursor.close()
        return 1

    def insert(self, table, column_values):
        try:
            cursor = self.con.cursor()
            columns = ", ".join(column_values.keys())
            values = tuple(column_values.values())
            param_markers = ", ".join(["?" for item in list(values)])
            SQL = f"INSERT INTO {table} ({columns}) VALUES ({param_markers});"
            cursor.execute(SQL, values)
            self.con.commit()
            cursor.close()
            return 1
        except Exception as e:
            print(e)

    def find(self, table, chat_id, column, value, columns):
        cursor = self.con.cursor()
        _columns = ", ".join(columns)
        SQL = f"SELECT {_columns} FROM {table} WHERE {column} LIKE ? AND authorId = ?;"
        cursor.execute(SQL, (value, chat_id))
        rows = cursor.fetchall()
        items = []
        for row in rows:
            obj = {}
            for index, column in enumerate(columns):
                obj[column] = row[index]
            items.append(obj)
        cursor.close()
        return items

    def update(self, table, id, chat_id, column_values):
        try:
            cursor = self.con.cursor()
            keys = column_values.keys()
            update_params = ", ".join([f"{key} = ?" for key in keys])
            values = tuple(column_values.values())
            SQL = f"UPDATE {table} SET {update_params} WHERE id = ? AND authorId = ?;"
            cursor.execute(SQL, (*values, id, chat_id))
            self.con.commit()
            cursor.close()
            return 1
        except Exception as e:
            print(e)

if __name__ == "__main__":
    import sqlite3
    con = sqlite3.connect("database.db")
    default_user = {"authorId": "555", "first_name": "555", "last_name":"555", "first_name_last_name":"555", "surname":"555", "project":"555", "position":"555", "avatar":"555"}

    db = Database(con)

    #db.update("users", 2, "320539961", default_user)
    #db.insert("users", default_user)

    #print(db.fetch("320539961", "users", ["first_name"]))
    print(db.find("320539961", "users", "first_name_last_name", f"%юрий%".upper(), ["first_name"]))
