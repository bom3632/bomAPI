import flask_bcrypt
import datetime
from app.main import db
import jwt

from app.main.config import key
from app.main.model.blacklist import BlacklistToken


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "hd_user_base"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)  # user ID
    email = db.Column(db.String(256), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)  # 수퍼유저(level=99)일때만 True
    user_role = db.Column(db.String(32), nullable=False)  # super / worker / inspector
    level_cd = db.Column(db.String(2), nullable=False)  # worker:01~10, inspector:11~20, super:99
    username = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    memo = db.Column(db.String(512))
    reg_id = db.Column(db.String(512), default='system')  # todo : admin 등록시 해당ID 필요
    reg_datetime = db.Column(db.DateTime)
    modify_id = db.Column(db.String(512))
    modify_datetime = db.Column(db.DateTime)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<user '{}'="">".format(self.username)


class UserDetail(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "hd_user_detail"

    # todo : team_id (foreign key) 추가
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), db.ForeignKey('hd_user_base.public_id'))  # user ID
    address = db.Column(db.String(256))
    phone_number = db.Column(db.String(32))
    memo = db.Column(db.String(512))
    reg_id = db.Column(db.String(512), default='system')
    reg_datetime = db.Column(db.DateTime)
    modify_id = db.Column(db.String(512))
    modify_datetime = db.Column(db.DateTime)

    def __repr__(self):
        return "<user Detail '{}'="">".format(self.public_id)
