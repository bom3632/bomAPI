from flask import request
from flask_restplus import Resource
from flask_jwt_extended import (
    JWTManager, jwt_required, jwt_optional, create_access_token, get_jwt_identity, get_jwt_claims)

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, get_a_user_with_email, get_all_users_detail

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    #@jwt_required
    def get(self):
        """List all registered users"""
        return get_all_users_detail()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404, 'User not found.')
        else:
            return user


@api.route('/email/<email>')
@api.param('email', 'The User\'s email address')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user with email')
    @api.marshal_with(_user)
    def get(self, email):
        """get a user given its identifier"""
        user = get_a_user_with_email(email)
        if not user:
            api.abort(404, 'User not found.')
        else:
            return user
