from pprint import pprint
from requests import delete


# Удаление пользователя с id=3
pprint(delete("http://127.0.0.1:5000/api/users/3").json())
