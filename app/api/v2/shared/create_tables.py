import psycopg2
from .config import conn


def create_tables():
    """
    Create all tables
    """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            firstname  VARCHAR(255) NOT NULL,
            lastname VARCHAR(255) NOT NULL,
            email VARCHAR(25) NOT NULL,
            role VARCHAR(25) NOT NULL,
            username VARCHAR(25) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS categories (
           cat_id SERIAL PRIMARY KEY,
           cat_name VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS products(
           product_id SERIAL PRIMARY KEY,
           prod_name VARCHAR(255) NOT NULL,
           prod_price VARCHAR(255) NOT NULL,
           instock INTEGER NOT NULL,
           max_purchasable INTEGER NOT NULL,
           cat_id INTEGER NOT NULL,
           FOREIGN KEY(cat_id)
              REFERENCES categories(cat_id)
              ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS sale_records (
            sale_id SERIAL PRIMARY KEY,
            sale_attendant VARCHAR(100) NOT NULL,
            product_name VARCHAR (255) NOT NULL,
            product_price VARCHAR(50) NOT NULL,
            quanity_sold VARCHAR(255) NOT NULL,
            total_amount VARCHAR(255) NOT NULL,
            product_id INTEGER NOT NULL,
            FOREIGN KEY (product_id)
                    REFERENCES products (product_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
            sale_date VARCHAR (100) NOT NULL
       )
        """
    )

    cur = conn.cursor()
    # Create table one by one
    for command in commands:
        cur.execute(command)
    cur.close()
    conn.commit()


if __name__ == '__main__':
    create_tables()
