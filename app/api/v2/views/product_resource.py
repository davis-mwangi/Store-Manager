from flask_restful import Resource, reqparse
from ..models.products_model import ProductModel
from flask_jwt_extended import jwt_required, get_jwt_claims

from ..shared.validation import (
    validate_product_name,
    numeric_only,
)


class ProductResource(Resource):
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

    @jwt_required
    def post(self, prod_id):
        claims = get_jwt_claims()
        if claims['role'] != 'admin':
            return {"message": "Admin privilege required"}, 401
        data = ProductResource.parser.parse_args()
        product = ProductModel.find_product_by_id(prod_id)
        if product:
            ProductModel.update_product(
                data['product_name'],
                data['product_price'],
                data['instock'],
                data['max_purchasable'],
                data['cat_id'],  prod_id,)
            return{"message": "Product Updated"}, 200
        return {"error": "failed to update, product not found"}, 404
