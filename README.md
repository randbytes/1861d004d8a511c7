# Установка окружения
```
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

# Установка переменных
В файле .env добавить обязательные значения для `BOT_TOKEN` и `BOT_USERNAME`(без @)

# Запуск
`python main.py`

## Настройка базы данных

```
touch database.db
sqlite3 database.db < sql/users.sql
```
