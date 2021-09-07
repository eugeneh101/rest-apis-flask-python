import sqlite3

from db import db


class UserModel(db.Model):  # this API (with 2 methods) is an interface for other parts of our program to interact with users
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)  # these are the columns actually stored in database; auto-incrementing
    username = db.Column(db.String(80))  # these are the columns actually stored in database
    password = db.Column(db.String(80))  # these are the columns actually stored in database

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM users WHERE username=?"
        # result = cursor.execute(query, (username,))  # need to be in a tuple
        # row = result.fetchone()
        # if row:
        #     user = cls(*row)  # user = cls(row[0], row[1], row[2])
        # else:
        #     user = None
        # connection.close()
        # return user

        # cls.query -> SELECT users.id AS users_id, users.username AS users_username, users.password AS users_password FROM users
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM users WHERE id=?"
        # result = cursor.execute(query, (_id,))  # need to be in a tuple
        # row = result.fetchone()
        # if row:
        #     user = cls(*row)  # user = cls(row[0], row[1], row[2])
        # else:
        #     user = None
        # connection.close()
        # return user

        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):  # upsert
        db.session.add(self)
        db.session.commit()
