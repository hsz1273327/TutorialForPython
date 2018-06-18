#coding:UTF-8
from flask import Flask,request,g,make_response,abort,redirect,url_for,render_template,flash,session
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask_wtf.csrf import CsrfProtect#新增
import time

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField 
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True
bootstrap = Bootstrap(app)
manager = Manager(app)
csrf = CsrfProtect(app)

#新增
class MoneyForm(Form):
    money = StringField('How much RMB to change?', validators=[Required()])
    submit = SubmitField('Submit')

@app.template_filter('RMBtoUSD')
def RMBtoUSD(text):
    return "$"+str(round(float(text)*0.1520,2))


@app.before_request
def before_request():
        g.time = time.asctime()
#删除一些
@app.errorhandler(404)
def page_not_found(error):
    return "404,page not found!",404,{"a":"af"}
#需要注册http方法
@app.route('/',methods = ["GET","POST"])
def hello():
    ##修改
    old_money = "0"
    money = "0"
    moneyform = MoneyForm()
    if moneyform.validate_on_submit():
        old_money = session.get('money')
        
        if moneyform.money.data:
            money = str(moneyform.money.data)
            session["money"]=money
        if money == "0":
            flash("Looks like you entered 0")
            session["money"]=money
            return redirect(url_for('hello'))                   
        moneyform.money.data =""
        
    response = make_response(render_template('myapp/index.html',count=g.time,
                                             moneyform=moneyform,
                                             answer=old_money+"元",money=money))
    response
    return response

@app.route('/<name>')
def name(name):
    return "time:{count} Hello, world! - {name}".format(count=g.time,name=name)

@app.route("/info")
def info():
    user_agent = request.headers.get('User-Agent')
    return '<p>time:{count}</p><p>Your browser is {agent}</p>'.format(count=g.time,agent=user_agent)

@app.route('/login')
def login():
    abort(404)
@app.route('/infos')
def infos():
    return redirect(url_for('info'))
@app.route("/changimg")
def changimg():
    return '''<p> 图片</p>'''
