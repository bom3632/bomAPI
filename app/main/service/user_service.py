import datetime

from app.main import db
from app.main.model.user import User


# 사용자 추가
def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=data['public_id'],
            email=data['email'],
            username=data['username'],
            password=data['password'],
            level_cd=data['level_cd'],
            user_role=data['user_role'],
            reg_datetime=datetime.datetime.utcnow(),
            memo="",
        )
        if data['level_cd'] == '99':    # super admin
            new_user.is_admin = True
        else:
            new_user.is_admin = False

        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User email already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        print('auth_token:', auth_token)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
