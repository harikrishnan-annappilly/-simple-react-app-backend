from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, get_current_user, get_jti, get_jwt, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import UserModel

BLACKLIST = {-1,}

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help='username')
_user_parser.add_argument('password', type=str, required=True, help='password')
_user_parser.add_argument('role', type=str)

class User(Resource):
    def post(self):
        payload = _user_parser.parse_args()
        username = payload['username']
        password = payload['password']
        role = payload['role'] if payload['role'] else 'default from function'
        if UserModel.find_by_username(username=username):
            return {'message': 'username already taken'}
        user = UserModel(username=username, password=password, role=role)
        user.save()
        return user.json()

    def delete(self):
        payload = _user_parser.parse_args()
        username = payload['username']
        user = UserModel.find_by_username(username=username)
        if user:
            user.delete()
        return {'message': 'user deleted'}


class UserLogin(Resource):
    def post(self):
        payload = _user_parser.parse_args()
        username = payload['username']
        password = payload['password']
        user = UserModel.find_by_username(username=username)
        if user and user.password == password:
            additional_claims = {
                'role': user.role
            }
            access_token = create_access_token(identity=user.id, fresh=True, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

class Users(Resource):
    def get(self):
        return {
            'users': [
                u.json() for u in UserModel.query.all()
            ]
        }
    
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user_identity = get_jwt_identity()
        non_fresh_access_token = create_access_token(
                                                    identity=current_user_identity,
                                                    fresh=False
                                                    )
        return {
            'access-token': non_fresh_access_token,
        }

class RevokeAccess(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {
            'message': 'user logged out'
        }
