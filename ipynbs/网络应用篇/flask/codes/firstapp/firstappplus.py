#coding:UTF-8
from flask import Flask
from flask.ext.script import Manager

app = Flask(__name__)
app.debug = True
manager = Manager(app)

@app.route('/')
def hello():
    return "Hello, world! - flask"

@app.route('/<name>')
def name(name):
    return "Hello, world! - {name}".format(name=name)