from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
# import sqlite3
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(  # like argparse
        "price",
        type=float,
        required=True,
        help="This field cannot be left blank!",
    )
    parser.add_argument(  # like argparse
        "store_id",
        type=int,
        required=True,
        help="Every item needs a store id",
    )


    # @app.route("/student/<string:name>")
    @jwt_required()  # need access token
    def get(self, name):
#         item = next(filter(lambda x: x["name"] == name, items), None)
#         if item is not None:
#             return {"item": item}, 200 if item else 404
# #         for item in items:
# #             if item["name"] == name:
# #                 return item
#         return {"item": None}, 404  # don't need to raise an Exception
# #        return {"student": name}  # don't need to jsonify? Yes, due to flask_restful
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()  # return item
        return {"message": "Item not found"}, 404
        
    def post(self, name):  # has to be same signature as get()
#         # request_data = request.get_json(force=True)  # do not need content type header
#         # request_data = request.get_json(silent=True)  # doesn't give error, returns None
#         if next(filter(lambda x: x["name"] == name, items), None):
#             return {"message": f"An item with name '{name}' already exists"}, 400  # bad request

# #         request_data = request.get_json()  # separate the name from the price
#         # price = request_data["price"]
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name} already exists"}, 400

        data = Item.parser.parse_args()  # how do these functions get the data without arguments?
        # item = {"name": name, "price": data["price"]}
        item = ItemModel(name, **data)
        try:
            # ItemModel.insert(item)
            # item.insert()
            item.save_to_db()
        except Exception as e:
            return {"message": "An error occurred inserting the item"}, 500  # internal server error

        return item.json(), 201  # it appears that 200 is default status code

    def put(self, name):  # idempotent action
        # data = request.get_json()  # how do these functions get the data without arguments?
        data = Item.parser.parse_args()  # how do these functions get the data without arguments?
#         item = next(filter(lambda x: x["name"] == name, items), None)
        item = ItemModel.find_by_name(name)
        # updated_item = {"name": name, "price": data["price"]}
        # updated_item = ItemModel(name, data["price"])
        if item is None:
#             item = {"name": name, "price": data["price"]}
#             items.append(item)
            # try:
            #     # ItemModel.insert(updated_item)
            #     updated_item.insert()
            # except:
            #     return {"message": "An error occurred inserting the item"}, 500
            item = ItemModel(name, **data) 
        else:
#             item.update(data)
            # try:
            #     # ItemModel.update(updated_item)
            #     updated_item.update()
            # except:
            #     return {"message": "An error occurred inserting the item"}, 500
            item.price = data["price"]
            item.store_id = data["store_id"]
        item.save_to_db()  # insert or update
        # return updated_item.json()
        return item.json()

    def delete(self, name):  # should the delete body be moved to ItemModel? no
#         global items  # allows "mutating" list
#         items = list(filter(lambda x: x["name"] != name, items))

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        # return {"message": "Item deleted"}

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted"}

class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({"name": row[0], "price": row[1]})
        # connection.close()
        
        # return {"items": items}  # must return a dictionary    

#         return {"items": [item.json() for item in ItemModel.query.all()]}
        return {"items": [item.json() for item in ItemModel.find_all()]}