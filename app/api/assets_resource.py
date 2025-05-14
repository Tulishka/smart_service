from flask import jsonify
from flask_restful import abort

from app import db
from app.api.common import BaseResource, pagination, pagination_response
from app.api.parsers.assets import asset_update_parser, asset_parser
from app.assets.models import Asset, AssetType


class AssetResource(BaseResource):
    def get(self, asset_id):
        """Получение асета по id"""
        asset = Asset.query.get_or_404(asset_id)
        return jsonify(self._asset_to_dict(asset))

    def put(self, asset_id):
        """Обновление асета"""
        args = asset_update_parser.parse_args()
        asset = Asset.query.get_or_404(asset_id)

        if 'type_id' in args and args['type_id'] is not None:
            # Проверка существования вида асета
            if not AssetType.query.get(args['type_id']):
                abort(404, message=f"Вид асета с id = {args['type_id']} не найден")

        for key, value in args.items():
            if value is not None:
                setattr(asset, key, value)

        db.session.commit()
        return jsonify(self._asset_to_dict(asset))

    def delete(self, asset_id):
        """Удаление асета"""
        asset = Asset.query.get_or_404(asset_id)
        if len(asset.tickets) == 0:
            db.session.delete(asset)
            db.session.commit()
            return jsonify({'message': 'Асет удален!'})
        return abort(400, message='Асет не может быть удален, используется в заявках!')

    @classmethod
    def _asset_to_dict(cls, asset):
        return {
            'id': asset.id,
            'name': asset.name,
            'type_id': asset.type_id,
            'address': asset.address,
            'uid': str(asset.uid),
            'image': asset.image,
            'status': asset.status.value,
            'details': asset.details,
            'type_name': str(asset.type) if asset.type else None
        }


class AssetListResource(BaseResource):
    def get(self):
        """Получение всех асетов"""

        assets = pagination(Asset.query)
        return pagination_response(assets, [AssetResource._asset_to_dict(a) for a in assets.items])

    def post(self):
        """Создание нового асета"""
        args = asset_parser.parse_args()

        # Проверка существования вида асета
        if not AssetType.query.get(args['type_id']):
            abort(404, message=f"Вид асета с id = {args['type_id']} не найден")

        asset = Asset(
            name=args['name'],
            type_id=args['type_id'],
            address=args['address'],
            uid=args['uid'],
            image=args.get('image'),
            status=args['status'],
            details=args.get('details')
        )

        db.session.add(asset)
        db.session.commit()
        return jsonify(AssetResource._asset_to_dict(asset))


class AssetTypeResource(BaseResource):
    def get(self):
        """Получение всех видов асетов"""
        types = AssetType.query.all()
        return jsonify([{
            'id': t.id,
            'name': t.name,
            'description': t.description,
            'image': t.image,
            'qr_help_text': t.qr_help_text
        } for t in types])
