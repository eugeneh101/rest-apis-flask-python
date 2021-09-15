# import sqlite3  # because using flask_sqlalchemy via "db" object

from db import db

class StoreModel(db.Model):

    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)  # these are the columns actually stored in database
    name = db.Column(db.String(80))  # these are the columns actually stored in database

    items = db.relationship("ItemModel", lazy="dynamic")  # back reference
    # lazy=dynamic makes it so self.items is not list of items but a query builder
    # tradeoff is speed of calling json method and speed of creating store

    def __init__(self, name):
        # what happens to the id?
        self.name = name

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.json() for item in self.items.all()],
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM __tablename__ WHERE name=name LIMIT 1;

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):  # upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()