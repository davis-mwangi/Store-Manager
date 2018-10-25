
from flask import Flask, jsonify, Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager

from .api.v2.shared.create_tables import create_tables
from .api.v2.views.user_resource import (
    UserLogin,
    UserRegister
)
from .api.v2.views.product_resource import ProductResource


blueprint = Blueprint('store_manager', __name__)
api = Api(blueprint, catch_all_404s=True, prefix='/api/v2')


api.add_resource(UserLogin, '/auth/login')
api.add_resource(UserRegister,  '/auth/signup')
api.add_resource(ProductResource, '/products/<int:prod_id>')


app = Flask(__name__)
app.secret_key = 'David'
app.register_blueprint(blueprint)

jwt = JWTManager(app)
# Create tables when the app is run
create_tables()


@app.route('/')
def index():
    return jsonify({"message": "Welcome to My Store Manager API"})


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    if identity[2] == 'admin':
        role = 'admin'
    else:
        role = 'attendant'

    return {
        'username': identity[3],
        'role': role
    }


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification Failed',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    })
