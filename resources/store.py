from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": "Store not found"}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": f"A store with name `{name}` already exists"}, 400
        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred while creating the store."}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "Store deleted"}  # do we care if nothing was actually deleted?


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.find_all()]}
        # return {"stores": [store.json() for store in StoreModel.query.all()]}