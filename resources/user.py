# import sqlite3
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_raw_jwt,
    jwt_refresh_token_required,
    jwt_required,
)
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from blacklist import BLACKLIST
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(  # like argparse
    "username",
    type=str,
    required=True,
    help="This field cannot be left blank!",
)
_user_parser.add_argument(  # like argparse
    "password",
    type=str,
    required=True,
    help="This field cannot be left blank!",
)


class UserRegister(Resource):
    def post(self):
        data = (
            _user_parser.parse_args()
        )  # how do these functions get the data without arguments?
        if UserModel.find_by_username(data["username"]):
            return {"message": "Username already exists"}, 400

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "INSERT INTO users VALUES (NULL, ?, ?)"  # because auto-increment
        # cursor.execute(query, (data["username"], data["password"]))
        # connection.commit()
        # connection.close()
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found"}, 404
        user.delete_from_db()
        return {"message": "user deleted"}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()
        # find user in the database
        user = UserModel.find_by_username(data["username"])
        # check password
        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(
                identity=user.id, fresh=True
            )  # identity= is what `identity()` function used to do
            refresh_token = create_refresh_token(
                user.id
            )  # create refresh token (will look at this later)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200
        return {"message": "invalid credentials"}, 401
        # return them


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]  # JWT ID, unique identity for a JWT
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required  # works if refresh token passed in
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
