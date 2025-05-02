import qrcode
from app.config import Config
import os


def create_qr_if_need(asset_uid):
    if str(asset_uid) in [i.split(".")[0] for i in os.listdir("app/static/assets/qr")]:
        return
    web_address = f'{Config.APP_HOST}/tickets/new/{asset_uid}'
    img_address = f'app/static/assets/qr/{asset_uid}.png'
    img = qrcode.make(web_address)
    img.save(img_address)
    return True
