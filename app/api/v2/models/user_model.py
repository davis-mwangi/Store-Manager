import psycopg2

from ..shared.config import conn


class User(object):

    def __init__(self, _id, firstname, lastname, email, role, username,
                 password):
        self.id = _id,
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.role = role
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        user = None
        try:
            cursor = conn.cursor()

            query = """
                SELECT *
                FROM users WHERE username=%s;
                """
            cursor.execute(query, (username,))
            fetched_rows = cursor.fetchone()

            conn.commit()

            if fetched_rows is not None:
                # *row passes the columns as a set  arguments
                user = cls(*fetched_rows)
            else:
                user = None
            cursor.close()

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

        return user

    @classmethod
    def find_by_id(cls, _id):

        cursor = User.connection.cursor()

        query = "SELECT * FROM users WHERE id=%s"
        cursor.execute(query, (_id,))
        row = cursor.fetchone()
        if row is not None:
            user = cls(*row)
        else:
            user = None

        conn.close()
        return user

    @classmethod
    def save_to_db(cls, firstname, lastname, email, role, username, password):
        cursor = conn.cursor()
        query = """
                INSERT INTO users(firstname,lastname,email,role,username, \
                password) \
                VALUES (%s,%s,%s,%s,%s,%s);
                """
        cursor.execute(query, (firstname, lastname,
                               email, role, username, password))

        conn.commit()
        cursor.close()
