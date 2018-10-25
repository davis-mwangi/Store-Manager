from flask_restful import Resource, reqparse
from ..models.user_model import User
from werkzeug.security import safe_str_cmp


def check_blank(value):
    if value.strip() == "":
        raise ValueError("Cannot be blank")
    return value


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=check_blank,
                        required=True,
                        )
    parser.add_argument("password",
                        type=check_blank,
                        required=True,
                        )

    @classmethod
    def post(cls):
        data = UserLogin.parser.parse_args()
        # find user in database
        user = User.find_by_username(data['username'])
        # check password
        if user and safe_str_cmp(user.password, data['password']):
            return 200

        return {'message': 'Invalid credentials'}, 401
