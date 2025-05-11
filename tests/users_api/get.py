from pprint import pprint
import requests

# Получение всех пользователей
pprint(requests.get(
    "http://127.0.0.1:5000/api/users?apikey=CD3rlxIXQ0pGVrE72r1n33MBhH1Q5I4xd2eTgHOxBbq9HTN5BdVVZ4c3gfgNlY0").json())

print("=" * 20)

# Получение пользователя с id=1
pprint(requests.get(
    "http://127.0.0.1:5000/api/users/1?apikey=CD3rlxIXQ0pGVrE72r1n33MBhH1Q5I4xd2eTgHOxBbq9HTN5BdVVZ4c3gfgNlY0").json())

print("=" * 20)

# Запрос к получению юзера с отсутствующим ключом
pprint(requests.get("http://127.0.0.1:5000/api/users/1").json())

# Запрос к получению юзера с неверным ключом
pprint(requests.get("http://127.0.0.1:5000/api/users/1?apikey=12").json())

print('=' * 20)


# Запрос на получение пользователя с ошибочным id
pprint(requests.get(
    "http://127.0.0.1:5000/api/users/2232?apikey=CD3rlxIXQ0pGVrE72r1n33MBhH1Q5I4xd2eTgHOxBbq9HTN5BdVVZ4c3gfgNlY0")
       .json())
