import json
from main import main
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/<string:name>/', methods = ['GET'])
def hello(name):
    x = name.replace("+", " ")
    obj = json.loads(main(x))
    return obj
app.run(host="34.123.94.67", port="5000")

