from flask_restful import Resource, reqparse
from ..models.user import User
from .authy import auth
import re


EMAIL_REGEX = re.compile(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$')
SPECIAL_CHARS = '[@_!#$%^&*()<>?/\|}{~:]'


def email(value):
    if value.strip() == "":
        raise ValueError("Email cannot be blank")

    if not EMAIL_REGEX.match(value):
        raise ValueError("Invalid email format")

    return value


def validate_name(value):
    if value.strip() == "":
        raise ValueError("Name cannot be blank")

    if not value.isalpha():
        raise ValueError("Invalid name")

    return value


def validate_password(password):

    if not any(char.isdigit() for char in password):
        raise ValueError('password should have at least one numeral')

    if not any(char.isupper() for char in password):
        raise ValueError(
            'password should have at least one uppercase letter')

    if not any(char.islower() for char in password):
        raise ValueError(
            'the password should have at least one lowercase letter')

    if not any(char in SPECIAL_CHARS for char in password):
        raise ValueError(
            'password should have at least one special character e.g $%$#')
    if len(password) < 8:
        raise ValueError(
            'length of password should be 8 charatcers or more')
    return password


class UserResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
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

    @auth.login_required
    def post(self):
        for user in User.users:
            if user.role == 'attendant' and auth.username():
                return {'message': 'Not authorised to acess'}, 401

            if user.role == 'admin' and auth.username() == user.username:
                data = UserResource.parser.parse_args()

                if next(filter(lambda x: x.username == data['email']
                               .split('@')[0], User.users), None):
                    return {'message': 'store attendant already exists'}, 400

                user_id = {'id': user.id for user in User.users}

                user = User(1,
                            data['name'], data['email'],
                            data['email'].split('@')[0], data['password'],
                            'attendant')
                user.save_user()
                return {"message": "New user created successfully"}, 201
