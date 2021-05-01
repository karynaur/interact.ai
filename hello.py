import json
from main import main
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/<string:name>/')
def hello(name):
    x = name.replace("+", " ")
    obj = json.loads(main(x))
    return obj
app.run()

