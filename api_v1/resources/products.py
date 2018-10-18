from flask_restful import Resource, reqparse
from .authy import auth
from .users import User


products = [
    {
        'product_id': 1,
        'product_name': 'dell laptop',
        'price': 70000,
        'instock': 5,
        'category': 'computers'
    },
    {
        'product_id': 2,
        'product_name': 'iphone 7',
        'price': 50000,
        'instock': 10,
        'category': 'smart phones $ electronics'
    },

]


class ProductsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_name',
                        type=str,
                        required=True,
                        help='Product name cannnot be blank')
    parser.add_argument('price',
                        type=str,
                        required=True,
                        help='Price cannnot be blank')
    parser.add_argument('instock',
                        type=int,
                        required=True,
                        help='In stock cannot  be blank')
    parser.add_argument('category',
                        type=str,
                        required=True,
                        help='Category name cannnot be blank')

    @auth.login_required
    def post(self):
        """
        Check if the authenticated user has 'admin' or 'attendant' role
        If 'admin' authorize, else if 'attendant' deny access
        """
        data = ProductsResource.parser.parse_args()
        for user in User.users:
            if user.role == 'attendant' and user.email == auth.username():
                return {'message': 'Not authorised to access '}
            if user.role == 'admin' and user.email == auth.username():
                if next(filter(lambda x: x['product_name'] ==
                               data['product_name'], products), None):
                    return {'message': 'Product Already exists'}, 400

                product = {'product_id': products[-1].get('product_id') + 1,
                           'product_name': data['product_name'],
                           'price': data['price'], 'instock': data['instock'],
                           'category': data['category']}
                products.append(product)
                return {'message': 'New product created'}, 201

    @auth.login_required
    def get(self):
        return {"products": products}, 200


class ProductResource(Resource):
    @auth.login_required
    def get(self, product_id):
        product = next(filter(lambda x: x['product_id'] == product_id,
                              products), None)
        if product:
            return {'product': product}
        return {"error": "Product with id {} is not found"
                .format(product_id)}, 404
