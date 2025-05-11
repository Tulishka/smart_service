from pprint import pprint
import requests

# Получение всех пользователей
pprint(requests.get("http://127.0.0.1:5000/api/users").json())

print("=" * 20)

# Получение пользователя с id=1
pprint(requests.get("http://127.0.0.1:5000/api/users/1").json())

print("=" * 20)

# Запрос к получению юзера с несуществующим id
pprint(requests.get("http://127.0.0.1:5000/api/users/421412").json())
