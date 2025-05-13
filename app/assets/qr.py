"""
Модуль для работы с QR кодами

"""


import os

import qrcode

from app.config import Config

# Создаем папку для хранения QR
os.makedirs(f"app/{Config.MEDIA_FOLDER}/qr", exist_ok=True)


def create_qr_if_need(asset_uid) -> bool | None:
    """Функция, создающая QR в случае необходимости

    :param asset_uid: Уникальный идентификатор асета
    :return: True в случае успешного добавления / None - если асет существует
    """

    # Если QR для этого асета существует - ничего не выполняем
    if os.path.exists(f"{Config.MEDIA_FOLDER}/qr"):
        return

    web_address = f'{Config.APP_HOST}/tickets/new/{asset_uid}'
    img_address = f'app/{Config.MEDIA_FOLDER}/qr/{asset_uid}.png'
    img = qrcode.make(web_address)
    img.save(img_address)
    return True
