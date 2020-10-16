import datetime

from flask import jsonify
from sqlalchemy import text

from app.main import db
from app.main.model.user import User, UserDetail


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
        if data['level_cd'] == '99':  # super admin
            new_user.is_admin = True
        else:
            new_user.is_admin = False
        user_detail = UserDetail(
            public_id=data['public_id'],
            address=data['address'],
            phone_number=data['phone_number'],
            reg_datetime=datetime.datetime.utcnow(),
        )
        save_changes(new_user, user_detail)  # insert to DB
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User email already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    # return User.query.all()
    users = db.engine.execute(text("""
            select * from flask_test.hd_user_base
            """)).fetchall()

    return [{
        'public_id': row['public_id'],
        'user_role': row['user_role'],
        'level_cd': row['level_cd'],
        'email': row['email'],
    } for row in users]


def get_all_users_detail():
    # return db.session.query(User).\
    #     outerjoin(UserDetail, User.public_id == UserDetail.public_id).\
    #     all()
    # ORM , outer join이 잘 안된다.
    users = db.engine.execute(text("""
        select *
            from flask_test.hd_user_base
            left  join  flask_test.hd_user_detail
            on hd_user_base.public_id = hd_user_detail.public_id
            """)).fetchall()

    return [{
        'public_id': row['public_id'],
        'username': row['username'],
        'password': row['password_hash'],
        'user_role': row['user_role'],
        'level_cd': row['level_cd'],
        'email': row['email'],
        'address': row['address'],
        'phone_number': row['phone_number'],
    } for row in users]


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def get_a_user_with_email(email):
    return User.query.filter_by(email=email).first()


def save_changes(data, detail):
    db.session.add(data)
    db.session.add(detail)
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
