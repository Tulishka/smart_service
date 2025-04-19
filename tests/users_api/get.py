from pprint import pprint
import requests

with requests.Session() as session:
    # Вход в систему под данными первого пользователя
    pprint(session.post("http://127.0.0.1:5000/api/login", json={"phone": "+222", "password": "12345"}).json())

    print("--" * 20)

    # Получение всех пользователей
    pprint(session.get("http://127.0.0.1:5000/api/users").json())

    print("--" * 20)

    # Получение пользователя с id=1
    pprint(session.get("http://127.0.0.1:5000/api/users/1").json())
