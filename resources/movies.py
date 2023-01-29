from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from models.movies import MovieModel

# title = db.Column(db.String(20), unique=True, nullable=False)
# numberInStock = db.Column(db.Integer, nullable=False)
# dailyRentalRate = db.Column(db.Float(precision=2), nullable=False)
# liked = db.Column(db.Boolean, default=False, nullable=False)
# genre_id = db.Column(db.Integer)


class Movie(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help='enter "title"')
    parser.add_argument('numberInStock', type=int,
                        required=True, help='enter "numberInStock"')
    parser.add_argument('dailyRentalRate', type=float,
                        required=True, help='enter "dailyRentalRate"')
    parser.add_argument('liked', type=bool, help='enter "liked"')
    parser.add_argument('genreId', type=int, required=True,
                        help='enter "genreId"')

    # @jwt_required()
    def get(self, id):
        movie = MovieModel.find_by_id(id)
        if movie:
            return movie.json()
        return {
            'message': 'item not found'
        }, 404

    def put(self, id):
        movie = MovieModel.find_by_id(id)
        if movie:
            movie.title = self.parser.parse_args()['title'] or movie.title
            movie.numberInStock = self.parser.parse_args(
            )['numberInStock'] or movie.numberInStock
            movie.dailyRentalRate = self.parser.parse_args(
            )['dailyRentalRate'] or movie.dailyRentalRate
            movie.liked = self.parser.parse_args()['liked'] or movie.liked
            movie.genre_id = self.parser.parse_args()[
                'genreId'] or movie.genre_id
            movie.save()
            return movie.json()
        return {
            'message': 'movie not found'
        }, 404

    # @jwt_required()
    def delete(self, id):
        # claims = get_jwt()
        # if claims['role'] != 'admin':
        #     return {
        #         'message': 'No permission to use this'
        #     }, 401
        movie = MovieModel.find_by_id(id)
        if movie:
            movie.delete()
            return {
                'message': 'item deleted'
            }, 200
        return {
            'message': 'item not found'
        }, 404


class Movies(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help='enter "title"')
    parser.add_argument('numberInStock', type=int,
                        required=True, help='enter "numberInStock"')
    parser.add_argument('dailyRentalRate', type=float,
                        required=True, help='enter "dailyRentalRate"')
    parser.add_argument('liked', type=bool,
                        help='enter "liked"')
    parser.add_argument('genreId', type=int, required=True,
                        help='enter "genreId"')
    # @jwt_required(optional=True)

    def get(self):
        # current_identity = get_jwt_identity()
        return [
            i.json() for i in MovieModel.find_all()
        ]

    def post(self):
        title = self.parser.parse_args()['title']
        # movie = MovieModel.find_by_title(title)
        if MovieModel.find_by_title(title):
            return {
                'message': f'movie with title {title} already exist'
            }, 400
        movie = MovieModel(
            title=self.parser.parse_args()['title'],
            numberInStock=self.parser.parse_args()['numberInStock'],
            dailyRentalRate=self.parser.parse_args()['dailyRentalRate'],
            liked=self.parser.parse_args()['liked'],
            genre_id=self.parser.parse_args()['genreId'],
        )
        movie.save()
        print('movie saved')
        return movie.json()
