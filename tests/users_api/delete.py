from pprint import pprint
import requests


# Удаление пользователя с id=3
pprint(requests.delete("http://127.0.0.1:5000/api/v1/users/3?apikey=___SECRET____API__KEY___1").json())
