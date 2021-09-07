import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(  # like argparse
        "username",
        type=str,
        required=True,
        help="This field cannot be left blank!",
    )
    parser.add_argument(  # like argparse
        "password",
        type=str,
        required=True,
        help="This field cannot be left blank!",
    )

    def post(self):
        data = UserRegister.parser.parse_args()  # how do these functions get the data without arguments?
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
