from pprint import pprint
import requests


with requests.Session() as session:
    # Вход в систему под данными первого пользователя
    pprint(session.post("http://127.0.0.1:5000/api/login", json={"phone": "+222", "password": "12345"}).json())

    print("--" * 20)

    # Изменение департаммента второго пользователя на департамент с id=1 и пароля на 54321
    print(session.put("http://127.0.0.1:5000/api/users/2", json={
        "department_id": 2,
        "password": "12345"
    }).json())
