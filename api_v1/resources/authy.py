from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import safe_str_cmp
from ..models.user import User

auth = HTTPBasicAuth()


@auth.error_handler
def auth_error():
    return jsonify({'message': 'Access denied'}), 401


@auth.verify_password
def get_password(username, password):
    return authenticate(username, password)


def authenticate(username, password):
    for user in User.users:
        if user.username == username and safe_str_cmp(
                user.password, password):
            return user
