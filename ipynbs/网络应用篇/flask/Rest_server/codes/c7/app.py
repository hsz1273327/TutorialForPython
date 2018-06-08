# --*-- coding:utf-8 --*--
from flask import Flask,request,jsonify
from flask_restful import Api,Resource
import json
from itsdangerous import URLSafeSerializer as USer

app = Flask(__name__)
api = Api(app)

import os

from peewee import SqliteDatabase
db = SqliteDatabase(os.path.abspath("peewee_db.sqlite"))
from peewee import Model,CharField,DateField,BooleanField,ForeignKeyField
class User(Model):
    name = CharField()
    password = CharField()
    type = CharField(default="local")
    
    SER = USer("secret",salt="salt1")
    def __str__(self):
        return "<USER: id-{self.id}--name-{self.name}>".format(self=self)
    def __repr__(self):
        return self.__str__()
    
    def verify_password(self,target):
        return True if self.SER.loads(self.password) == target else False
    @staticmethod
    def hash_password(org):
        return User.SER.dumps(org)
    class Meta:
        database = db # 确定使用的是哪个db,方便多种数据库配合使用
        
db.connect() 
try:
    db.create_tables([User])
except:
    print " * db is ready"
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message":"404 not found","code":404}), 404

class UsersAPI(Resource):
    
    def get(self):
        result = [user.__str__() for user in list(User.select())]
        return {"result":result}

    def post(self):
        data = json.loads(request.data)
        user = User(name = data.get("name"),password =User.hash_password(data.get("password"))).save()
        return jsonify({"result":"save {name} done!".format(name=data.get("name"))})
    
class UserAPI(Resource):

    def get(self,user_id):
        
        user = User.get(User.id==user_id)
        if not user:
            abort(404)
            
        result = {"name":user.name,"password":user.password,"type":user.type}
        return jsonify({"result":result})
    
  
    def put(self,user_id):
        data = request.args
        user = User.get(User.id==user_id)
        if request.args.get("name"):
            user.name=data.get("name")
        if request.args.get("password"):
            user.password=User.hash_password(data.get("password"))
        user.save()
        
        return jsonify({"result":"update {name} done!".format(name=user_id)})  

    def delete(self,user_id):
        
        User.get(User.id==user_id).delete_instance() 
        return jsonify({"result":"delete {id} done!".format(id=user_id)})  
    
    
api.add_resource(UsersAPI, '/users/')        
api.add_resource(UserAPI, '/user/<int:user_id>')  

if __name__ == '__main__':
    app.run(debug=True)