from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    TABLE_NAME = "items"
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()

        # item = {"name": name, "price": data["price"]}
        item = ItemModel(name, data["price"])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}

        return item

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data["price"])
        if item is None:
            # try:
            #     updated_item.save_to_db()
            # except:
            #     return {"message": "An error occurred inserting the item."}
            item = ItemModel(name, data["price"])
        else:
            # try:
            #     updated_item.save_to_db()
            # except:
            #     raise
            #     return {"message": "An error occurred updating the item."}
            item.price = data["price"]
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    TABLE_NAME = "items"

    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
        # return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}

