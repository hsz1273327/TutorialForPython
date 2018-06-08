# --*-- coding:utf-8 --*--
from __future__ import print_function, unicode_literals, division

from flask import Flask,jsonify,request
from flask_restaction import Resource, Api, Gen, Res
import json

app = Flask(__name__)
api = Api(app)
res = Res(api)

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
             
    def toDict(self):
        return {"id": self._id,
        "name": self.name,
        "password": self.password,
        "type":self.type}
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message":"404 not found","code":404}), 404


class Users(Resource):
    paging = {
        "pagenum": "+int&default=1",
        "pagesize": "int(5,50)&default=10"
    }
    info = {
        "id": "+int&required",
        "name": "safestr&required",
        "password": "safestr&required",
        "type":"safestr&required"
    }
    schema_inputs = {
        "get": {"user_id": "+int&required"},
        "post": {
            "name": ("safestr&required", "your name"),
            "password":("safestr&required", "your password")
        },
        "put": {
            "user_id": "+int&required",
            "name": "safestr",
            "password": "safestr"
        },
        "delete": {"user_id": "+int&required"}
    }
    schema_outputs = {
        "get": info,
        "get_list": [info],
        "post": info,
        "put": info,
        "delete": {"message": "unicode"}
    }
    def get(self,user_id):
        try:
            user = filter(lambda x:True if x._id==user_id else False,Userlist)[0]
        except IndexError as e:
            abort(404)
        return user.toDict()
    
    def get_list(self):
        return map(lambda x:x.toDict(),Userlist)
        
    def post(self,name,password):
        print(name)
        user = User(name,password)
        return user.toDict()
    
     
    def put(self,user_id,name,password):
        user = filter(lambda x: True if x._id==user_id else False,Userlist)[0]
        if name:
            user.name=name
        if password:
            user.password=password
        
        return user.toDict()
    def delete(self,user_id):
        global Userlist
        Userlist = filter(lambda x: False if x._id==user_id else True,Userlist)
        return {"message": "OK"}
        
api.add_resource(Users)

gen = Gen(api)
gen.resjs('static/js/res.js')
gen.resdocs('static/resdocs.html', resjs='/static/js/res.js',
                bootstrap='/static/css/bootstrap.min.css')

if __name__ == '__main__':
    app.run(debug=True)