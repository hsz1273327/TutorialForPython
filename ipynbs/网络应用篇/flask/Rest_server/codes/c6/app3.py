# --*-- coding:utf-8 --*--
from flask import Flask,request,jsonify
from flask_restful import Api,Resource
import json

app = Flask(__name__)
api = Api(app)

import redis
User = redis.StrictRedis(host='localhost', port=6379, db=0)
        
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message":"404 not found","code":404}), 404

class UsersAPI(Resource):
    
    def get(self):
        result = zip(User.keys(),map(lambda x:User.hgetall(x),User.keys()))
        return {"result":result}

    def post(self):
        _id = max(map(lambda x:int(x),User.keys()))+1
        data = json.loads(request.data)
        data["type"]="local"
        User.hmset(_id,data)
        return jsonify({"result":"save {name} done!".format(name=data.get("name"))})
    
class UserAPI(Resource):

    def get(self,user_id):
        
        user = User.hgetall(user_id)
        if not user:
            abort(404)
            

        return jsonify({"result":user})
    
  
    def put(self,user_id):
        data = request.args
        user = User.hgetall(user_id)
        if not request.args.get("name"):
            data["name"]=user.get("name")
            
        if not request.args.get("password"):
            data["password"]=user.get("password")
            
        User.hmset(user_id,data)
        
        return jsonify({"result":"update {name} done!".format(name=user_id)})  

    def delete(self,user_id):
        
        User.delete(user_id)
        return jsonify({"result":"delete {id} done!".format(id=user_id)})  
    
    
api.add_resource(UsersAPI, '/users/')        
api.add_resource(UserAPI, '/user/<int:user_id>')  

if __name__ == '__main__':
    app.run(debug=True)