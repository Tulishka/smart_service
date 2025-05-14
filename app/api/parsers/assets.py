from flask_restful import reqparse

from app.assets.models import AssetStatus

asset_parser = reqparse.RequestParser()
asset_parser.add_argument('name', type=str, required=True, help='name обязательное поле')
asset_parser.add_argument('type_id', type=int, required=True, help='type_id обязательное поле')
asset_parser.add_argument('address', type=str, required=True, help='address обязательное поле')
asset_parser.add_argument('uid', type=str, required=True, help='uid обязательное поле')
asset_parser.add_argument('image', type=str)
asset_parser.add_argument('status', type=str, choices=[s.value for s in AssetStatus],
                          default=AssetStatus.ACTIVE.value)
asset_parser.add_argument('details', type=str)

asset_update_parser = reqparse.RequestParser()
asset_update_parser.add_argument('name', type=str)
asset_update_parser.add_argument('type_id', type=int)
asset_update_parser.add_argument('address', type=str)
asset_update_parser.add_argument('image', type=str)
asset_update_parser.add_argument('status', type=str, choices=[s.value for s in AssetStatus])
asset_update_parser.add_argument('details', type=str)
