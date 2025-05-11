from pprint import pprint
import requests


# Добавление пользователя с именем чебурашка
print(requests.post(
    "http://127.0.0.1:5000/api/users?apikey=CD3rlxIXQ0pGVrE72r1n33MBhH1Q5I4xd2eTgHOxBbq9HTN5BdVVZ4c3gfgNlY0", json={
        "name": "cheburashka",
        "phone": 88005553535,
        "password": "12345"}).json())
