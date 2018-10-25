from flask import Flask, jsonify, Blueprint
from flask_restful import Api


from .api.v1.models.user import User
from .api.v1.views.users import UserResource
from .api.v1.views.products import ProductsResource, ProductResource
from .api.v1.views.sales import SalesResource, SaleResource


blueprint = Blueprint('store_manager', __name__)
api = Api(blueprint, catch_all_404s=True, prefix='/api/v1')


# Create an admin
User.users.append(User(1, 'david mwangi', 'david398@gmail.com',
                       'david398', 'David2018$$', 'admin'))

# Create  store attendant
User.users.append(User(2, 'julius mwangi', 'julius2018@gmail.com',
                       'julius2018', 'Julius2018@', 'attendant'))


api.add_resource(UserResource, '/register')
api.add_resource(ProductsResource, '/products')
api.add_resource(ProductResource, '/products/<int:product_id>')
api.add_resource(SalesResource, '/sales')
api.add_resource(SaleResource, '/sales/<int:sale_id>')


app = Flask(__name__)
app.secret_key = 'David'
app.register_blueprint(blueprint)


@app.route('/')
def index():
    return jsonify({"message": "Welcome to My Store Manager API"})
