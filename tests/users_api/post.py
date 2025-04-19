from pprint import pprint
from requests import post

# Добавление пользователя с именем чебурашка
print(post("http://127.0.0.1:5000/api/users", json={
    "name": "cheburashka",
    "phone": 88005553535,
    "password": "12345"
}).json())
