import os

from flask import Flask
from flask_jwt_extended import JWTManager  # from flask_jwt import JWT
from flask_restful import Api  # Resource usually mapped to database tables

from db import db
from resources.item import Item, ItemList
from resources.store import Store, StoreList
# from security import authenticate, identity
from resources.user import User, UserLogin, UserRegister

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.db"
).replace("postgres://", "postgresql://")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "jose"  # app.config["JWT_SECRET_KEY"]
api = Api(app)


# jwt = JWT(app, authenticate, identity)  # /auth for access token
jwt = JWTManager(
    app
)  # not creating /auth endpoint, so have to create it ourselves; in this case /login


@jwt.user_claims_loader
def add_claims_to_jwt(
    identity,
):  # must take in 1 argument called "identity" when using this decorator
    if (
        identity == 1
    ):  # instead of hard coding, should read from config file or database
        return {"is_admin": True}
    return {"is_admin": False}


api.add_resource(Item, "/item/<string:name>")  # http://127.0.0.1/5000/student/Rolf
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")

if __name__ == "__main__":
    db.init_app(app)
    app.run(
        port=5000,
        debug=True,  # helpful error messages
    )
    # Test-first API design where put API calls in Postman first and then code up API endpoints
