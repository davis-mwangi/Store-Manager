from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_claims,
    get_raw_jwt
)
from werkzeug.security import safe_str_cmp

from ..models.user_model import User
from ..shared.validation import (
    validate_name,
    validate_password,
    check_blank,
    email
)


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

    def post(self):
        data = UserLogin.parser.parse_args()
        # find user in database
        user = User.find_by_username(data['username'])
        user_obj = (user.firstname, user.lastname,
                    user.role, user.username)
        # check password
        if user and safe_str_cmp(user.password, data['password']):
            # create access token
            access_token = create_access_token(
                identity=user_obj)
            return{
                'access_token': access_token
            }, 200

        # return them
        return {'message': 'Invalid credentials'}, 401


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname',
                        type=validate_name,
                        required=True
                        )
    parser.add_argument('lastname',
                        type=validate_name,
                        required=True
                        )

    parser.add_argument('email',
                        type=email,
                        required=True,
                        )

    parser.add_argument('password',
                        type=validate_password,
                        required=True,
                        )

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        if claims['role'] != 'admin':
            return {"message": "Admin privilege required"}, 401

        data = UserRegister.parser.parse_args()
        username = data['email'].split('@')[0]
        user = User.find_by_username(username)

        if User.find_by_username(username):
            return {'message': 'store attendant already exists'}, 400

        # If doesnt exist create e a new user
        User.save_to_db(data['firstname'], data['lastname'], data['email'],
                        'attendant', username, data['password'])

        return {"message": "New user created successfully"}, 201


