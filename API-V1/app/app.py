from flask import Flask, jsonify, Blueprint
from flask_restful import Api


from models.user import User
from resources.users import UserResource


blueprint = Blueprint('store_manager', __name__)
api = Api(blueprint, prefix='/api/v1')


# Create an admin
User.users.append(User(1, 'david', 'mwangi',
                       'david@gmail.com', 27, '0700111222',
                       'david', 'admin'))

# Create  store attendant
User.users.append(User(2, 'julius', 'mwangi', 'julius@gmail.com',
                       35, '0723000777', 'julius', 'attendant'))


api.add_resource(UserResource, '/register')


app = Flask(__name__)
app.secret_key = 'David'
app.register_blueprint(blueprint)
