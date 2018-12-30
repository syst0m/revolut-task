import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True



@app.route('/', methods=['GET'])
def home():
    return "<h1>Birthday API</h1><p>This site is an API for storing/retrieving user's birthday information</p>"

app.run()
