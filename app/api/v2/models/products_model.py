from ..shared.config import conn


class ProductModel(object):

    def __init__(self, _id, prod_name, prod_price, instock, max_purchasable,
                 category):
        self.id = _id,
        self.prod_name = prod_name
        self.prod_price = prod_price
        self.instock = instock
        self.max_purchasable = max_purchasable
        self.category = category

    @classmethod
    def find_product_by_id(cls, _id):

        cursor = conn.cursor()

        query = """
            SELECT product_id,prod_name,prod_price,instock,max_purchasable,
             cat_name
            FROM products
            INNER JOIN  categories  ON categories.cat_id = products.cat_id
            WHERE product_id=%s
            """
        cursor.execute(query, (_id,))
        row = cursor.fetchone()
        if row is not None:
            prod = cls(*row)
        else:
            prod = None
        return prod

    # return dictionary
    def json(self):
        return {
            'id': self.id,
            'prod_name': self.prod_name,
            'prod_price': self.prod_price,
            'instock': self.instock,
            'max-purchasable': self.max_purchasable,
            'category': self.category
        }

    @classmethod
    def update_product(cls, name, price, instock, purchasable,
                       category, _id,):
        """
        Update product based on the product id
        """
        query = """UPDATE products
                SET prod_name=%s, prod_price=%s,instock=%s,
                max_purchasable=%s,cat_id=%s
                WHERE product_id=%s
                """
        cursor = conn.cursor()
        cursor.execute(query, (name, price, instock, purchasable,
                               category, _id))
        conn.commit()
        cursor.close()

    def delete_product(self, prod_id):
        rows_deleted = 0
        try:

            cur = conn.cursor()
            query = "DELETE FROM products WHERE product_id=%s"
            cur.execute(query, (prod_id,))
            conn.commit()
            cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
