from flask import Flask
from flask_restful import Api  # Resource usually mapped to database tables
from flask_jwt import JWT

from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "jose"
api = Api(app)

@app.before_first_request  # truly lazy
def create_tables():
    db.create_all()  # no longer need create_tables.py


jwt = JWT(app, authenticate, identity)  # /auth for access token

api.add_resource(Item, "/item/<string:name>")  # http://127.0.0.1/5000/student/Rolf
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    db.init_app(app)
    app.run(
        port=5000,
        debug=True,  # helpful error messages
    )
    # Test-first API design where put API calls in Postman first and then code up API endpoints
