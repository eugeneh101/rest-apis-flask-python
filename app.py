import os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager  # from flask_jwt import JWT
from flask_restful import Api  # Resource usually mapped to database tables

from blacklist import BLACKLIST
from db import db
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import TokenRefresh, User, UserLogin, UserLogout, UserRegister

# from security import authenticate, identity

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.db"
).replace("postgres://", "postgresql://")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "jose"  # app.config["JWT_SECRET_KEY"]
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]


@app.before_first_request  # truly lazy
def create_tables():
    db.create_all()  # no longer need create_tables.py


api = Api(app)
api.add_resource(Item, "/item/<string:name>")  # http://127.0.0.1/5000/student/Rolf
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")


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


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST
    # if True, then goes to revoked_token_callback()


@jwt.expired_token_loader
def expired_token_callback():
    return (
        jsonify({"description": "This token has expired", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"description": "Signature verification failed", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not have an access token",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return (
        jsonify(
            {"description": "The token is not fresh", "error": "fresh_token_required"}
        ),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback():
    return (
        jsonify(
            {"description": "The token has been revoked", "error": "token_revoked"}
        ),
        401,
    )


if __name__ == "__main__":
    db.init_app(app)
    app.run(
        port=5000,
        debug=True,  # helpful error messages
    )
    # Test-first API design where put API calls in Postman first and then code up API endpoints
