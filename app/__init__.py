
from flask import Flask, jsonify, Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager

from .api.v2.shared.create_tables import create_tables
from .api.v2.views.user_resource import UserLogin, UserRegister

blueprint = Blueprint('store_manager', __name__)
api = Api(blueprint, catch_all_404s=True, prefix='/api/v2')


api.add_resource(UserLogin, '/auth/login')
api.add_resource(UserRegister,  '/auth/signup')


app = Flask(__name__)
app.secret_key = 'David'
app.register_blueprint(blueprint)

jwt = JWTManager(app)
# Create tables when the app is run
create_tables()


@app.route('/')
def index():
    return jsonify({"message": "Welcome to My Store Manager API"})