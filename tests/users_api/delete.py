from pprint import pprint
import requests


# Удаление пользователя с id=3
pprint(requests.delete("http://127.0.0.1:5000/api/users/3").json())
