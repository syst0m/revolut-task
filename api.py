from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

# test data

users = [
    {
    'name':'John',
    'dateOfBirth':'2000-01-01'
    }
]

class User(Resource):
    def get(self, name):
        for user in users:
            if(name == user["name"]):
                return user, 200
        return "User not found", 404

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("dateOfBirth")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["dateOfBirth"] = args["dateOfBirth"]
                return user, 200

        user = {
            "name": name,
            "dateOfBirth": args["dateOfBirth"]
                }
        users.append(user)
        return user, 204

api.add_resource(User, "/hello/<string:name>")

app.run()
