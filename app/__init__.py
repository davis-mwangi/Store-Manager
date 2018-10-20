from flask import Flask, jsonify, Blueprint
from flask_restful import Api


from .api.v1.models.user import User
from .api.v1.views.users import UserResource
from .api.v1.views.products import ProductsResource, ProductResource
from .api.v1.views.sales import SalesResource, SaleResource


blueprint = Blueprint('store_manager', __name__)
api = Api(blueprint, prefix='/api/v1')


# Create an admin
User.users.append(User(1, 'david mwangi', 'david@gmail.com',
                       'david398', 'david', 'admin'))

# Create  store attendant
User.users.append(User(2, 'julius mwangi', 'julius@gmail.com',
                       'julius2018', 'julius', 'attendant'))


api.add_resource(UserResource, '/register')
api.add_resource(ProductsResource, '/products')
api.add_resource(ProductResource, '/products/<int:product_id>')
api.add_resource(SalesResource, '/sales')
api.add_resource(SaleResource, '/sales/<int:sale_id>')


app = Flask(__name__)
app.secret_key = 'David'
app.register_blueprint(blueprint)
