from flask_restful import Resource, reqparse
from models.user import User
from .authy import auth


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help='First name cannnot be blank')
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help='Last name cannnot be blank')
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help='Email cannnot be blank')
    parser.add_argument('age',
                        type=int,
                        required=True,
                        help='Age cannnot be blank')
    parser.add_argument('phone_number',
                        type=int,
                        required=False,
                        help='First name cannnot be blank')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='Password name cannnot be blank')

    @auth.login_required
    def post(self):
        for user in User.users:
            if user.role == 'attendant' and auth.username():
                return {'message': 'Not authorised to acess'}, 401

            if user.role == 'admin' and auth.username() == user.email:
                data = UserResource.parser.parse_args()
                # Check if the user exists
                if next(filter(lambda x: x.email == data['email'],
                               User.users), None):
                    return {'message': 'store attendant already exists'}, 400

                # If doesnt exist create  a new Store attendant
                user_id = {'id': user.id for user in User.users}
                # print(int(user.get('id') or 0)+1)
                user = User(1,
                            data['first_name'], data['last_name'],
                            data['email'], data['age'],
                            data['phone_number'], data['password'],
                            'attendant')
                user.save_user()
                return {"message": "New user created successfully"}, 201
