import sqlite3
from flask import Flask
from flask_restful import Api, Resource, reqparse
from json import dumps
from datetime import datetime

# initialize app
app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

users = []

# initialize database
conn = sqlite3.connect('birthday.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (name VARCHAR, dateOfBirth VARCHAR)')
conn.commit()

conn.close()

def split_dob(dob):
    b_year = int(dob[0:4])
    b_month = int(dob[5:7])
    b_day = int(dob[8:10])

    birthday = datetime(b_year, b_month, b_day)
    return birthday

def calculate_days(birthday_date, now):
    delta1 = datetime(now.year, birthday_date.month, birthday_date.day)
    delta2 = datetime(now.year+1, birthday_date.month, birthday_date.day)
    days = (max(delta1, delta2) - now).days

    return days

def display_message(dob, days, name):
    today = datetime.today()
    current_month = int(f"{today:%m}")
    current_day = int(f"{today:%d}")

    b_month = int(dob[5:7])
    b_day = int(dob[8:10])

    if (current_day == b_day and current_month == b_month):
        message = "Hello, {}! Happy birthday!".format(name)
        return message
    else:
        message = "Hello, {}! Your birthday is in {} days".format(name,days)
        return message

class User(Resource):
    def get(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("dateOfBirth")
        args = parser.parse_args()

        #for user in users:
        #if(name == user["name"]):
        n = name
        conn = sqlite3.connect('birthday.sqlite')
        cur = conn.cursor()
        cur.execute("SELECT dateOfBirth FROM users WHERE name='{name}'".format(name=n))
        dob_tuple = cur.fetchone()
        conn.commit()
        #dob = user["dateOfBirth"]
        #name = user["name"]
        dob =  ''.join(dob_tuple)
        bd = split_dob(dob)
        today = datetime.today()
        c = calculate_days(bd, today)
        m = display_message(dob,c,name)
        serialized_message = dumps(m, default=str)

        user = {
            "name": name,
            "message": serialized_message
        }
        return  user, 200
        #return "User not found", 404

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("dateOfBirth")
        args = parser.parse_args()

        '''for user in users:
            if(name == user["name"]):
                user["dateOfBirth"] = args["dateOfBirth"]
                return user, 200
        '''
        user = {
            "name": name,
            "dateOfBirth": args["dateOfBirth"]
                }

        conn = sqlite3.connect('birthday.sqlite')
        cur = conn.cursor()
        cur.execute('INSERT INTO users (name,dateOfBirth) VALUES (?, ?)',
            (user["name"], user["dateOfBirth"]))
        conn.commit()

        users.append(user)
        return user, 204

api.add_resource(User, "/hello/<string:name>")

app.run(host='0.0.0.0')
