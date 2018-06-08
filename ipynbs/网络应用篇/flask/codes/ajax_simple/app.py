#coding:UTF-8
from flask import Flask,jsonify, render_template, request,url_for
from flask.ext.script import Manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

manager = Manager(app)



@app.route('/',methods = ["GET","POST"])
def hello():
    return render_template('index.html')

@app.route('/ajax',methods = ["GET"])
def ajax():
    return jsonify({"hello":"hello world !"})