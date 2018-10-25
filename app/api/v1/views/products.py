from flask_restful import Resource, reqparse
from .authy import auth
from .users import User
import re

products = []


NUMERIC_REGEX = re.compile(r"^[0-9]+$")


def check_blank(value):
    if value.strip() == "":
        raise ValueError("{}cannot be blank {}".format(value))
    return value


def numeric_only(value):
    check_blank(value)
    if not NUMERIC_REGEX.match(value):
        raise ValueError("Only numbers required for this field")
    return value


def validate_product_name(value):
    check_blank(value)
    if value.isdigit():
        raise ValueError("Product name  cannot be numerics only")
    return value


class ProductsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_name',
                        type=validate_product_name,
                        required=True,
                        )
    parser.add_argument('product_price',
                        type=numeric_only,
                        required=True,
                        )
    parser.add_argument('instock',
                        type=numeric_only,
                        required=True,
                        )
    parser.add_argument('max_purchasable',
                        type=numeric_only,
                        required=True,
                        )
    parser.add_argument('cat_id',
                        type=numeric_only,
                        required=True,
                        )

    @auth.login_required
    def post(self):
        """
        Check if the authenticated user has 'admin' or 'attendant' role
        If 'admin' authorize, else if 'attendant' deny access
        """
        data = ProductsResource.parser.parse_args()
        for user in User.users:
            if user.role == 'attendant' and user.username == auth.username():
                return {'message': 'Not authorised to access '}, 401

            if user.role == 'admin' and user.username == auth.username():
                if next(filter(lambda x: x['product_name'] ==
                               data['product_name'], products), None):
                    return {'message': 'Product Already exists'}, 400

                product = {'product_id': products[-1].get('product_id') + 1
                           if len(products) > 0 else 1,
                           'product_name': data['product_name'],
                           'product_price': data['product_price'],
                           'instock': data['instock'],
                           'max_purchasable': data['max_purchasable'],
                           'cat_id': data['cat_id']}
                products.append(product)
                return {'message': 'New product created'}, 201

    @auth.login_required
    def get(self):
        if len(products) == 0:
            return {"message": "No products found"}, 404
        return {"products": products}, 200


class ProductResource(Resource):
    @auth.login_required
    def get(self, product_id):
        if len(products) == 0:
            return {"error": "no products in store"}, 404
        product = next(filter(lambda x: x['product_id'] == product_id,
                              products), None)
        if product:
            return {'product': product}
        return {"error": "Product with id {} is not found"
                .format(product_id)}, 404
