import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from db import db
from resources.item import Item, Items
from resources.user import RevokeAccess, User, UserLogin, Users, TokenRefresh

app = Flask(__name__)

app.secret_key = 'keytobeused'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)),'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

api = Api(app)

migrate = Migrate(app, db)

jwt = JWTManager(app)

@jwt.invalid_token_loader
def invalid_token_entered(response):
    return jsonify({
        'response': response,
        'message': 'invalid token entered hari coded this'
    })

from resources.user import BLACKLIST

@jwt.token_in_blocklist_loader
def check_blocklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST

# this is optional only
@jwt.revoked_token_loader
def revoked_token_response(jwt_header, jwt_payload):
    return jsonify({
        'message': 'revoked access'
    })

@app.before_first_request
def create_all_tables():
    db.create_all()

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

api.add_resource(User, '/user')
api.add_resource(UserLogin, '/login')
api.add_resource(Users, '/users')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(RevokeAccess, '/revoke')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
