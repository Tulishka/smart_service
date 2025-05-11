from pprint import pprint
import requests


# Добавление пользователя с именем чебурашка
print(requests.post("http://127.0.0.1:5000/api/users", json={
    "name": "cheburashka",
    "phone": 88005553535,
    "password": "12345"
}).json())
