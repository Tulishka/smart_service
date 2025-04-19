from pprint import pprint
from requests import get


# Получение всех пользователей
pprint(get("http://127.0.0.1:5000/api/users").json())

print("--" * 20)

# Получение пользователя с id=1
pprint(get("http://127.0.0.1:5000/api/users/1").json())
