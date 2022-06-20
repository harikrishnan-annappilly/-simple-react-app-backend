from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='dumbass')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {
            'message': 'item not found'
        }, 404

    @jwt_required(fresh=True)
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {
                'message': f'item {name} already exists'
            }, 400
        item = ItemModel(name=name, price=self.parser.parse_args()['price'])
        item.save()
        return item.json()

    def put(self, name):
        item = ItemModel.find_by_name(name)
        price = self.parser.parse_args()['price']
        if item:
            item.price = price
        else:
            item = ItemModel(name=name, price=price)
        item.save()
        return item.json()

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if claims['role'] != 'admin':
            return {
                'message': 'No permission to use this'
            }, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
        return {
            'message': 'item deleted'
        }, 200

class Items(Resource):
    @jwt_required(optional=True)
    def get(self):
        current_identity = get_jwt_identity()
        return {
            'logged in': (current_identity if current_identity else -1),
            'message' : 'jwt optinal using here',
            'items': [
                i.json() for i in ItemModel.find_all()
            ]
        }
