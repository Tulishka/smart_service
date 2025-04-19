from pprint import pprint
import requests


with requests.Session() as session:
    # Вход в систему под данными первого пользователя
    pprint(session.post("http://127.0.0.1:5000/api/login", json={"phone": "+222", "password": "12345"}).json())

    # Добавление пользователя с именем чебурашка
    print(session.post("http://127.0.0.1:5000/api/users", json={
        "name": "cheburashka",
        "phone": 88005553535,
        "password": "12345"
    }).json())
