from flask_restful import Resource, reqparse
from .users import User
from .authy import auth
import datetime
from .products import products

sales = []


class SalesResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_name',
                        type=str,
                        required=True,
                        help="product name  cannot be blank")
    parser.add_argument('items_sold',
                        type=int,
                        required=True,
                        help="quantity cannot be blank")

    @auth.login_required
    def post(self):
        """
        Check if the authenticated user has 'admin' or 'attendant' role
        If attendant authorize, else if admin deny access
        """
        data = SalesResource.parser.parse_args()
        for user in User.users:
            if user.role == 'admin' and user.username == auth.username():
                return {'error': 'Not authorised to access'}, 401

            if user.role == 'attendant' and user.username == auth.username():
                if len(products) == 0:
                    return {"error": "No products in the store"}, 404

                for product in products:
                    if product['product_name'] == data['product_name']:
                        if int(product['instock']) >= data['items_sold']:
                            if data['items_sold'] >= 1:
                                sale_date = datetime.datetime.now() \
                                    .strftime("%B %d, %Y %H:%M %p")

                                total_amount = int(
                                    product['product_price']) * \
                                    int(data['items_sold'])

                                sale_record = {
                                    'sale_id': sales[-1]
                                    .get('sale_id') + 1
                                    # prevent index out of range error
                                    if len(sales) > 0 else 1,
                                    'sale_date': sale_date,
                                    'attendant_id': auth.username(),
                                    'product_name': data['product_name'],
                                    'product_price': product['product_price'],
                                    'products_sold': data['items_sold'],
                                    'total_amount': total_amount
                                }
                                sales.append(sale_record)

                                product['instock'] = int(
                                    product['instock']) - int(data['items_sold'])

                                return {'message': 'New Sale record created'}, 201
                            return {'error': 'Items sold  must be greater than 0'}, 400

                        return {"message": "only {} {} available in stock"
                                .format(product['instock'],
                                        product['product_name'])}

                    return {'message': 'No product found'}, 201

    @auth.login_required
    def get(self):
        """
        Check if the authenticated user has 'admin' or 'attendant' role
        If admin authorize, else if attendant deny access
        """
        for user in User.users:
            if user.role == 'attendant' and user.username == auth.username():
                return {'message': 'Not authorised to access '}, 401

            if user.role == 'admin' and user.username == auth.username():
                if len(sales) == 0:
                    return {"message": "No sales found"}, 404
                return {"sales": sales}, 200


class SaleResource(Resource):
    @auth.login_required
    def get(self, sale_id):
        for user in User.users:
            if user.role == 'attendant' and user.username == auth.username():
                sale = next(filter(lambda x: x['sale_id'] == sale_id and
                                   x['attendant_id'] == auth.username(),
                                   sales), None)
                if sale is not None:
                    return sale
                return {'error': 'sale record not found'}, 404

            if user.role == 'admin' and user.username == auth.username():
                sale = next(filter(lambda x: x['sale_id'] == sale_id,
                                   sales), None)
                if sale is not None:
                    return sale
                return {'error': 'sale record not found'}, 404
