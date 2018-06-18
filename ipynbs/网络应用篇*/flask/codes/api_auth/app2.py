# --*-- coding:utf-8 --*--
from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime, timedelta
app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

DELAY = 60

users = {
    "john": {"password":"hello","signed":None},
    "susan": {"password":"bye","signed":None}
}
TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

SIGNER = Serializer('secret-key',DELAY)

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)

parser_verify = reqparse.RequestParser()
parser_verify.add_argument('user', type=str)
parser_verify.add_argument('password', type=str)   

@auth.verify_password
def verify_password(username, password):
    if password == "":
        obj = SIGNER.loads(bytes(username,'utf-8'))
        if obj.get('user') not in users:
            return False
        else: 
            if users.get(obj.get('user')).get("password") == obj.get('password'):
                auth.me = obj.get('user')
                return True  
            else:
                return False
    else:
        if username not in users:
            return False
        else:
            if users.get(username).get("password") == password:
                auth.me = auth.username()
                return True  
            else:
                return False
        
        
class Verify(Resource):
    def post(self):
        args = parser_verify.parse_args()
        user = args['user']
        password = args['password']
        if user in users.keys():
            if (not users.get(user).get("signed")):
                if users.get(user).get("password")==password:
                    token = str(SIGNER.dumps({'user': user,'password':password}),'utf-8')
                    users.get(user)["signed"] = datetime.now()
                    return {"token":token}
                else:
                    abort(404, message="wrong password")
                    
                
            if users.get(user).get("signed")+ timedelta(seconds=DELAY) < datetime.now(): 
                if users.get(user).get("password")==password:
                    token = str(SIGNER.dumps({'user': user,'password':password}),'utf-8')
                    users
                    return {"token":token}
                else:
                    abort(404, message="wrong password")
            else:
                abort(404, message="your token has been signed")
        else:
            abort(404, message="user {} doesn't exist".format(user))
        

# Todo
#   show a single todo item and lets you delete them
class Todo(Resource):
    #decorators = [auth.login_required]
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
#   shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    decorators = [auth.login_required]
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201
    
class UserName(Resource):
    decorators = [auth.login_required]
    def get(self):
        return {"username":auth.me}

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(Verify, '/verify')
api.add_resource(UserName, '/username')

if __name__ == '__main__':
    app.run(debug=True)