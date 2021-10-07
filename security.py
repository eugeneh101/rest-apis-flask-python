# from resources.user import UserModel
# from werkzeug.security import safe_str_cmp

# # users = [{"id": 1, "name": "bob", "password": "asdf"}]
# # users = [
# #     User(1, "bob", "asdf"),
# # ]

# # username_mapping = {"bob": { "id": 1, "name": "bob", "password": "asdf"}}
# # username_mapping = {u.username: u for u in users}

# # userid_mapping = {1: {"id": 1, "name": "bob", "password": "asdf"}}
# # userid_mapping = {u.id: u for u in users}


# def authenticate(username, password):
#     user = UserModel.find_by_username(username)  # username_mapping.get(username)
#     if user and safe_str_cmp(user.password, password):
#         return user

# def identity(payload):  # Flask JWT
#     user_id = payload["identity"]
#     return UserModel.find_by_id(user_id)
#     # return userid_mapping.get(user_id, None)
