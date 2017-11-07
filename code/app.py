#!/home/pi/API_Class/venv/bin/python3
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
# Show items in items
    def get(self, name):
        for item in items:
            if item["name"] == name:
                return item
        return {"item": None}, 404 #error code 404 NOT FOUND

# Add items to your list
    def post(self, name):
        data = request.get_json()
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201 # Code 201 is for created

# Will show a list of all items
class ItemList(Resource):
    def get(self):
        return {"items": items}
        
api.add_resource(Item, "/item/<string:name>") 
api.add_resource(ItemList, "/items")

app.run(host="0.0.0.0", port=5000, debug=True)
