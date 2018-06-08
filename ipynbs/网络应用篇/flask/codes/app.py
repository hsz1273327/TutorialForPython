#--*--coding:utf-8 --*--
from __future__ import absolute_import,division,print_function,unicode_literals
"""
A message board appliation.

Author:Huang Sizhe
Date:22/01/2016
License:MIT
======================================

留言板应用

作者:黄思喆
日期:2016年1月22日
本应用使用MIT许可证

"""
from datetime import datetime,timedelta, timezone
#=================导入模块=================
from flask import Flask,render_template,make_response,redirect,url_for,flash,request

from flask.ext.bootstrap import Bootstrap

from flask_wtf.csrf import CsrfProtect
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField ,PasswordField
from wtforms.validators import DataRequired, Email
#导入ORM模块
from flask.ext.sqlalchemy import SQLAlchemy
#密码加密
from flask.ext.bcrypt import Bcrypt,generate_password_hash 
from sqlalchemy.ext.hybrid import hybrid_property
#login
from flask.ext.login import UserMixin,LoginManager,login_user,logout_user,login_required,current_user


#=================载入插件=================
bootstrap = Bootstrap()
csrf = CsrfProtect()

db = SQLAlchemy()# 实例化ORM对象

bcrypt = Bcrypt()#加密
login_manager = LoginManager()


#=================应用设置=================
from config import config,BASE_URL
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    
    db.init_app(app)#初始化数据库
    bcrypt.init_app(app)#加密
    #login
    login_manager.init_app(app)
    login_manager.login_view =  "signin"
    return app

import os
app = create_app(os.getenv('FLASK_CONFIG') or 'default') 

#flask-login的回调函数,实现后可以使用current_user来代理访问以登录的用户
@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id == userid).first()

#================主体=====================

#---------------自定义表单验证--------------

from wtforms.validators import ValidationError

class Unique(object):
    def __init__(self, model, field, message=u'Already exist !'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

#----------------自定义过滤器--------------



#-----------------数据库对象---------------

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='role')
    
    def __repr__(self):
        return '''<Role: {id} name: {name}>'''.format(id = self.id,
                                  name = self.name)
    
#user用于登录还要继承UserMixin ,这样就不用自己写几个验证函数了
class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    message = db.relationship('Message', backref='user')
    
    #密码的写法:
    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)
    

    def __repr__(self):
        return '''<User: {id} 
        name: {name}
        role_id: {role_id}
        email: {email}>'''.format(id = self.id,
                                  name = self.name,
                                 role_id = self.role_id,
                                 email = self.email)
    def is_correct_password(self, plaintext):
        if bcrypt.check_password_hash(self._password, plaintext):
            return True

        return False
    
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<message: {id} - {time} - {content}>'.format(id = self.id,
                                                             time=self.timestamp,
                                                             content = self.content)


    
##----------------主页--------------------------
class SignUp_Form(Form):
    email = StringField('Your e-mail', 
                        validators=[DataRequired(),
                                    Email(), 
                                    Unique(User, 
                                           User.email, 
                                           message='This e-mail has been used. Please use another one.')])
                        
    username = StringField('Pickup a username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up for MSG Board')

@app.route('/',methods = ["GET","POST"])
def index():
    
    if current_user.is_authenticated:
        return redirect(url_for("msgboard"))
    if current_user.is_active:
        return redirect(url_for("signin"))
    form = SignUp_Form()
    if form.validate_on_submit():
        user = User(name = form.username.data,
                    password = form.password.data,
                    email = form.email.data,
                    role_id = Role.query.filter_by(name='User').first().id)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('app/index.html', form=form)
##----------------msgboard页--------------------

@app.template_filter('AuthorName')
def AuthorName(text):
    return User.query.filter_by(id=int(text)).first().name

@app.template_filter('LocalTime')
def LocalTime(text):
    #return text.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
    local_timezone = {"zh-cn":8}
    return text.replace(tzinfo=timezone.utc).\
               astimezone(timezone(timedelta(hours=local_timezone.get(request.headers["Accept-Language"],0))))\
    .strftime('%a, %b %d %H:%M')+" in utc+"+str(local_timezone.get(request.headers["Accept-Language"],0))
    

class MsgForm(Form):
    msg = StringField('The msg', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/msgboard',methods = ["GET","POST"])
@login_required
def msgboard():
    msgform = MsgForm()
    if msgform.validate_on_submit():
        
        msg = Message(content = msgform.msg.data,
                      author_id=current_user.id)
        db.session.add(msg)
        db.session.commit()
        msgform.msg.data = ''
        return redirect(url_for('msgboard'))
        
    response = make_response(render_template('app/msgboard.html',
                                             msgform=msgform,
                                             MSG = Message.query.all()))
    return response

##----------------注册页--------------------v


@app.route("/signup",methods = ["GET","POST"])
def signup():
    form = SignUp_Form()
    if form.validate_on_submit():
        user = User(name = form.username.data,
                    password = form.password.data,
                    email = form.email.data,
                    role_id = Role.query.filter_by(name='User').first().id)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('app/signup.html', form=form)


##----------------登录页--------------------v
                        


class SignIn_Form(Form):
    email = StringField('Your e-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
@app.route("/signin",methods = ["GET","POST"])
def signin():
    form = SignIn_Form()

    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first_or_404()
        if email.is_correct_password(form.password.data):
            login_user(email)

            return redirect(url_for('index'))
        else:
            return redirect(url_for('signin'))
    return render_template('app/signin.html', form=form)

##---------------退出登录--------------------v
                        
@app.route('/signout')
@login_required
def signout():
    logout_user()
    flash('You have been signed out.')
    return redirect(url_for('index'))