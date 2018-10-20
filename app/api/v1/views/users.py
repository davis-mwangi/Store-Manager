from flask_restful import Resource, reqparse
from ..models.user import User
from .authy import auth


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='Name cannnot be blank')
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help='Email cannnot be blank')
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='Email cannnot be blank')                    
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='Password name cannnot be blank')

    @auth.login_required
    def post(self):
        for user in User.users:
            if user.role == 'attendant' and auth.username():
                return {'message': 'Not authorised to acess'}, 401

            if user.role == 'admin' and auth.username() == user.username:
                data = UserResource.parser.parse_args()
                # Check if the user exists
                if next(filter(lambda x: x.username == data['username'],
                               User.users), None):
                    return {'message': 'store attendant already exists'}, 400

                # If doesnt exist create  a new Store attendant
                user_id = {'id': user.id for user in User.users}
                # print(int(user.get('id') or 0)+1)
                user = User(1,
                            data['name'], data['email'],
                            data['username'], data['password'],
                            'attendant')
                user.save_user()
                return {"message": "New user created successfully"}, 201
