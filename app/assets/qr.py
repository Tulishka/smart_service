import qrcode
from app.config import APP_HOST
import os


def create_qr_if_need(asset_id):
    if str(asset_id) in [i.split(".")[0] for i in os.listdir("app/static/assets/qr")]:
        return
    web_address = APP_HOST + "/tickets/new/" + str(asset_id)
    img_address = "app/static/assets/qr/" + str(asset_id) + ".png"
    img = qrcode.make(web_address)
    img.save(img_address)
