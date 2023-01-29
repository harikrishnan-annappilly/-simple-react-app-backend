from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from models.genres import GenreModel


class Genre(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                        help='enter genre name')

    # @jwt_required()
    def get(self, id):
        item = GenreModel.find_by_id(id)
        if item:
            return item.json()
        return {
            'message': 'item not found'
        }, 404

    # @jwt_required(fresh=True)
    # def post(self, id):
    #     if GenreModel.find_by_id(id):
    #         return {
    #             'message': f'item {id} already exists'
    #         }, 400
    #     item = GenreModel(name=self.parser.parse_args()['name'])
    #     item.save()
    #     return item.json()

    def put(self, id):
        item = GenreModel.find_by_id(id)
        name = self.parser.parse_args()['name']
        if item:
            item.name = name
        else:
            item = GenreModel(name=name)
        item.save()
        return item.json()

    # @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        if claims['role'] != 'admin':
            return {
                'message': 'No permission to use this'
            }, 401
        item = GenreModel.find_by_id(id)
        if item:
            item.delete()
        return {
            'message': 'item deleted'
        }, 200


class Genres(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                        help='enter genre name')
    # @jwt_required(optional=True)

    def get(self):
        # current_identity = get_jwt_identity()
        return [
            i.json() for i in GenreModel.find_all()
        ]

    def post(self):
        name = self.parser.parse_args()['name']
        if GenreModel.find_by_name(name):
            return {
                'message': f'item {name} already exists'
            }, 400
        genre = GenreModel(name=name)
        genre.save()
        return genre.json()
