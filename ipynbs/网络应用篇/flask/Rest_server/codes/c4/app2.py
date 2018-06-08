# --*-- coding:utf-8 --*--
from flask import Flask,request,jsonify
from flask_restful import Api,Resource
from functools import reduce
app = Flask(__name__)
api = Api(app)
todos = {"+":lambda *x:sum(x),
        "-":lambda *x:reduce(lambda i,j:i-j,x),
        "*":lambda *x:sum(x),
        "/":lambda *x:reduce(lambda i,j:i/j,x)
        }

class TodoSimple(Resource):
         
    def get(self,todo_id):
        return jsonify({todo_id:todos.get(todo_id,lambda x,y: "undefined")(10,5)})
         
    def put(self, todo_id):
        todos[todo_id] = eval(str(request.form['data']))
        return {todo_id: str(request.form['data'])}

api.add_resource(TodoSimple,
                 '/<string:todo_id>',
                '/api/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
