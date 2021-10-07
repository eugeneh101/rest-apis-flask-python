# import sqlite3  # because using flask_sqlalchemy via "db" object

from db import db


class ItemModel(db.Model):

    __tablename__ = "items"
    id = db.Column(
        db.Integer, primary_key=True
    )  # these are the columns actually stored in database
    name = db.Column(db.String(80))  # these are the columns actually stored in database
    price = db.Column(
        db.Float(precision=2)
    )  # these are the columns actually stored in database

    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id")
    )  # have to delete all items in a store before being able to delete store/almost like a folder
    store = db.relationship("StoreModel")

    def __init__(self, name, price, store_id):
        # what happens to the id?
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id,
        }

    @classmethod
    def find_by_name(cls, name):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        # if row:
        #     # return {"item": {"name": row[0], "price": row[1]}}
        #     return cls(*row)

        # returns ItemModel instance
        return cls.query.filter_by(
            name=name
        ).first()  # SELECT * FROM __tablename__ WHERE name=name LIMIT 1;

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # def insert(self):
    #     connection = sqlite3.connect("data.db")
    #     cursor = connection.cursor()
    #     query = "INSERT INTO items VALUES (?, ?)"
    #     cursor.execute(query, (self.name, self.price))
    #     connection.commit()
    #     connection.close()

    # def update(self):
    #     connection = sqlite3.connect("data.db")
    #     cursor = connection.cursor()
    #     query = "UPDATE items SET price=? WHERE name=?"
    #     cursor.execute(query, (self.price, self.name))
    #     connection.commit()
    #     connection.close()

    def save_to_db(self):  # upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
