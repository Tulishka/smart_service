import qrcode
from app.config import Config
import os


def create_qr_if_need(asset_uid):
    if os.path.exists(f"{Config.MEDIA_FOLDER}/qr"):
        return
    web_address = f'{Config.APP_HOST}/tickets/new/{asset_uid}'
    img_address = f'app/{Config.MEDIA_FOLDER}/qr/{asset_uid}.png'
    img = qrcode.make(web_address)
    img.save(img_address)
    return True
