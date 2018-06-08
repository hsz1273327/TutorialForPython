# --*-- coding:utf-8 --*--
from __future__ import print_function, unicode_literals, division

from flask import Flask,jsonify,request,abort
from flask.views import MethodView
import json
app = Flask(__name__)

Userlist = []
def inc(cls):
    counter = {"result":0}
    def wrap(*args):
        counter["result"]+=1
        result = cls(counter["result"],*args)
        global Userlist
        Userlist.append(result)
        return result
    return wrap
@inc
class User(object):
    def __str__(self):
        return "<USER: id-{self._id}-{self.name}>".format(self=self)
    def __repr__(self):
        return self.__str__()
    def __init__(self,_id,name,password,type="local"):
        self._id=_id
        self.name = name
        self.password = password
        self.type=type
        
        
        
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message":"404 not found","code":404}), 404

class UsersAPI(MethodView):
    
    def get(self):
        return jsonify({"result":map(lambda x:x.__str__(),Userlist)})
        
    def post(self):
        data = json.loads(request.data)
        user = User(data.get("name"),data.get("password"))
        return jsonify({"result":"save {name} done!".format(name=user.name)})
    
class UserAPI(MethodView):
    
    def get(self,user_id):
        try:
            user = filter(lambda x:True if x._id==user_id else False,Userlist)[0]
        except IndexError as e:
            abort(404)
            
        result = {"name":user.name,"password":user.password,"type":user.type}
        return jsonify({"result":result})
        
    def put(self,user_id):
        data = request.args
        user = filter(lambda x: True if x._id==user_id else False,Userlist)[0]
        if request.args.get("name"):
            user.name=data.get("name")
        if request.args.get("password"):
            user.password=data.get("password")
        
        return jsonify({"result":"update {name} done!".format(name=user_id)})    
    def delete(self,user_id):
        global Userlist
        Userlist = filter(lambda x: False if x._id==user_id else True,Userlist)
        return jsonify({"result":"delete {id} done!".format(id=user_id)})   
        

app.add_url_rule('/users/',view_func=UsersAPI.as_view('users'.encode("utf-8")))
app.add_url_rule('/user/<int:user_id>',view_func=UserAPI.as_view('user'.encode("utf-8")))

if __name__ == '__main__':
    app.run(debug=True)