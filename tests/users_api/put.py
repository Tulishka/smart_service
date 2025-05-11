from pprint import pprint
import requests


# Изменение департаммента третьего пользователя на департамент с id=3 и пароля на 12345
print(requests.put("http://127.0.0.1:5000/api/users/3", json={
    "department_id": 2,
    "password": "12345"
}).json())
