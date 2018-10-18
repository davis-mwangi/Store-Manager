from flask_restful import Resource, reqparse
from .users import User
from .authy import auth


sales = [
    {
        'sale_id': 1,
        'sale_date': '15/10/2018',
        'attendant_id': 'julius@gmail.com',
        'total_price': 150600,
        'products_sold': [
            {
                'id': 1,
                'product_name': 'sugar',
                'price_per_item': 200,
                'items_sold': 3,
                'total_amount': 600
            },
            {

                'id': 2,
                'product_name': 'dell laptop',
                'price_per_item': 50000,
                'items_sold': 3,
                'total_amount': 150000
            }
        ]
    },
    {
        'sale_id': 2,
        'sale_date': '15/10/2018',
        'attendant_id': 'stella@gmail.com',
        'total_price': 150600,
        'products_sold': [
            {
                'id': 1,
                'product_name': 'sugar',
                'price_per_item': 200,
                'items_sold': 3,
                'total_amount': 600
            },
            {

                'id': 2,
                'product_name': 'dell laptop',
                'price_per_item': 50000,
                'items_sold': 3,
                'total_amount': 150000
            }
        ]
    }
]


class SalesResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sale_date',
                        type=str,
                        required=True,
                        help="Date cannot be blank")
    parser.add_argument('total_price',
                        type=int,
                        required=True,
                        help="Total price cannot be blank")

    def products_sold_parse(self, products_sold):
        if type(products_sold) != list:
            raise ValueError('Expected a list')
        return products_sold

    parser.add_argument('products_sold',
                        action='append',
                        type=dict,
                        required=True,
                        help='Products cannot be blank')

    @auth.login_required
    def post(self):
        """
        Check if the authenticated user has 'admin' or 'attendant' role
        If attendant authorize, else if admin deny access
        """
        data = SalesResource.parser.parse_args()
        for user in User.users:
            if user.role == 'admin' and user.email == auth.username():
                return {'error': 'Not authorised to access'}, 401

            if user.role == 'attendant' and user.email == auth.username():
                if next(filter(lambda x:
                               x['attendant_id'] == auth.username() and
                               x['sale_date'] == data['sale_date'],
                               sales), None):
                    return {'error': 'Sale record already exists'}, 400

                sale_record = {'sale_id': sales[-1].get('sale_id') + 1,
                               'sale_date': data['sale_date'],
                               'attendant_id': auth.username(),
                               'total_price': data['total_price'],
                               'products_sold': data['products_sold']}
                sales.append(sale_record)
                return {'message': 'New Sale record created'}, 201

    @auth.login_required
    def get(self):
        """
        Check if the authenticated user has 'admin' or 'attendant' role
        If admin authorize, else if attendant deny access
        """
        for user in User.users:
            if user.role == 'attendant' and user.email == auth.username():
                return {'message': 'Not authorised to access '}, 401

            if user.role == 'admin' and user.email == auth.username():
                return {"sales": sales}, 200


class SaleResource(Resource):
    @auth.login_required
    def get(self, sale_id):
        """
        Check if the logged in user is admin or if it matches the
        attendant username
        """
        for user in User.users:
            if user.role == 'attendant' and user.email == auth.username():
                sale = next(filter(lambda x: x['sale_id'] == sale_id and
                                   x['attendant_id'] == auth.username(),
                                   sales), None)
                if sale is not None:
                    return sale
                return {'error': 'sale record not found'}, 404

            if user.role == 'admin' and user.email == auth.username():
                sale = next(filter(lambda x: x['sale_id'] == sale_id,
                                   sales), None)
                if sale is not None:
                    return sale
                return {'error': 'sale record not found'}, 404
