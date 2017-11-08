#!/home/pi/API_Class/venv/bin/python3

from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "testkey"
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):
    #authenticate before running GET
    #This would need to be added to each action if each action requires auth or token
    @jwt_required()
    #GET items in list
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item is not None else 404 #error code 404 NOT FOUND

# Add items to your list
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {"message": "An item with name '{}' already exists".format(name)}, 400

        data = request.get_json()
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201 # Code 201 is for created

    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "Item deleted"}

    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item



# Will show a list of all items
class ItemList(Resource):
    def get(self):
        return {"items": items}
        
api.add_resource(Item, "/item/<string:name>") 
api.add_resource(ItemList, "/items")

app.run(host="0.0.0.0", port=5000, debug=True)
