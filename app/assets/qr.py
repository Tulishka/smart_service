import qrcode
from app.config import Config
import os


def create_qr_if_need(asset_id):
    if str(asset_id) in [i.split(".")[0] for i in os.listdir("app/static/assets/qr")]:
        return
    web_address = f'{Config.APP_HOST}/tickets/new/{asset_id}'
    img_address = f'app/static/assets/qr/{asset_id}.png'
    img = qrcode.make(web_address)
    img.save(img_address)
