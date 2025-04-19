from pprint import pprint
from requests import get


# Получение всех пользователей
pprint(get("http://127.0.0.1:5000/api/users").json())
