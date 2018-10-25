
from flask import Flask, jsonify, Blueprint
from flask_restful import Api
from .api.v2.shared.create_tables import create_tables

blueprint = Blueprint('store_manager', __name__)
api = Api(blueprint, prefix='/api/v2')


app = Flask(__name__)
app.secret_key = 'David'
app.register_blueprint(blueprint)


# Create tables when the app is run
create_tables()


@app.route('/')
def index():
    return jsonify({"message": "Welcome to My Store Manager API"})
