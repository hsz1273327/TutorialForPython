# --*-- coding:utf-8 --*--
from flask import Flask,request,jsonify
from flask_restful import Api,Resource
import json

app = Flask(__name__)
api = Api(app)

import os

from pony import orm

db = orm.Database()
class User(db.Entity):
    name = orm.Required(unicode)
    password = orm.Required(unicode)
    type = orm.Required(unicode,default=u"local")
    
    def __str__(self):
        return "<USER: id-{self.id}--name-{self.name}>".format(self=self)
    def __repr__(self):
        return self.__str__()
    
db.bind('sqlite', os.path.abspath("pony_db.sqlite"),create_db=True)
db.generate_mapping(create_tables=True)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message":"404 not found","code":404}), 404

class UsersAPI(Resource):
    
    def get(self):
        with orm.db_session :
            result = map(lambda x:x.__str__(),User.select()[:])
        return {"result":result}
     
    @orm.db_session
    def post(self):
        data = json.loads(request.data)
        user = User(name = data.get("name"),password =data.get("password"))
        return jsonify({"result":"save {name} done!".format(name=user.name)})
    
class UserAPI(Resource):
    @orm.db_session
    def get(self,user_id):
        
        user = User.get(id=user_id)
        if not user:
            abort(404)
            
        result = {"name":user.name,"password":user.password,"type":user.type}
        return jsonify({"result":result})
    
    @orm.db_session   
    def put(self,user_id):
        data = request.args
        user =User.get(id=user_id)
        if request.args.get("name"):
            user.name=data.get("name")
        if request.args.get("password"):
            user.password=data.get("password")
        
        return jsonify({"result":"update {name} done!".format(name=user_id)})  
    @orm.db_session
    def delete(self,user_id):
        
        User.get(id=user_id).delete()
        return jsonify({"result":"delete {id} done!".format(id=user_id)})  
    
    
api.add_resource(UsersAPI, '/users/')        
api.add_resource(UserAPI, '/user/<int:user_id>')  

if __name__ == '__main__':
    app.run(debug=True)

