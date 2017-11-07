from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        for item in items:
            if item["name"] == name:
                return item
        return {"item": None}, 404 #error code 404 NOT FOUND


    def post(self, name):
        item = {"name": name, "price": 12.00}
        items.append(item)
        return item, 201 # Code 201 is for created



api.add_resource(Item, "/item/<string:name>") 

# Host app on Raspian host test from different machine
app.run(host="0.0.0.0", port=5000)
