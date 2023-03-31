from sanic import Sanic
from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json as jsonify
from jsonschema import validate

app = Sanic()
api_user = Blueprint('api_user')

User = []

User_Schema = {
    "title": "User",
    "description": "用户",
    "type": "object",
    "properties": {
        "name": {
            "description": "user name",
            "type": "string"
        }, "age": {
            "description": "user age",
            "type": "integer",
            "minimum": 0,
            "maximum": 140,
            "exclusiveMaximum": True
        }
    },
    "required": ["name", "age"]
}


class UserIndexAPI(HTTPMethodView):

    async def get(self, request):
        count = len(User)
        result = {
            "description": "测试api,User总览",
            "user-count": count,
            "links": [
                {
                    "uri": "/user",
                    "method": "POST",
                    "description": "创建一个新用户"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "GET",
                    "description": "用户号为<id>的用户信息"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "PUT",
                    "description": "更新用户号为<id>用户信息"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "DELETE",
                    "description": "删除用户号为<id>用户"
                },
            ]
        }

        return jsonify(result, ensure_ascii=False)

    async def post(self, request):
        insert = request.json

        try:
            validate(instance=insert, schema=User_Schema)
        except Exception as e:
            return jsonify({
                "msg": "参数错误",
                "error": str(e)
            }, ensure_ascii=False, status=401)
        else:
            uid = User.append(insert)
            return jsonify({
                "msg": "插入成功",
                "uid": uid
            }, ensure_ascii=False)


class UserAPI(HTTPMethodView):

    async def get(self, request, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }, ensure_ascii=False, status=401)

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }, ensure_ascii=False, status=500)
        else:
            if u:
                return jsonify(u, ensure_ascii=False)
            else:
                return jsonify({
                    "msg": "未找到用户",
                }, ensure_ascii=False, status=401)

    async def put(self, request, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }, ensure_ascii=False, status=401)

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }, ensure_ascii=False, status=500)
        else:
            if u:
                insert = request.json
                u.update(insert)
                return jsonify({
                    "msg": "更新成功"
                }, ensure_ascii=False)
            else:
                return jsonify({
                    "msg": "未找到用户",
                }, ensure_ascii=False, status=401)

    async def delete(self, request, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }, ensure_ascii=False, status=401)

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }, ensure_ascii=False, status=500)
        else:
            if u:
                User[uid] = None
                return jsonify({
                    "msg": "删除成功",
                }, ensure_ascii=False)
            else:
                return jsonify({
                    "msg": "未找到用户",
                }, ensure_ascii=False, status=401)


user_index_view = UserIndexAPI.as_view()
user_view = UserAPI.as_view()

api_user.add_route(user_index_view, '/user')
api_user.add_route(user_view, '/user/<uid:int>')


api_todo = Blueprint('api_todo')

Todo = {}

Todo_Schema = {
    "title": "Todo",
    "description": "工作列表",
    "type": "object",
    "properties": {
        "msg": {
            "description": "message",
            "type": "string"
        }, "dead_line": {
            "description": "dead line",
            "type": "str"
        }
    },
    "required": ["msg"]
}


class TodoAPI(HTTPMethodView):

    async def get(self, request, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }, ensure_ascii=False, status=401)

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }, ensure_ascii=False, status=500)
        else:
            if u:
                if Todo.get(uid):
                    return jsonify({"uid": uid, "todo": Todo.get(uid)}, ensure_ascii=False)
                else:
                    return jsonify({
                        "msg": "未找到用户的todo列表",
                    }, ensure_ascii=False, status=404)
            else:
                return jsonify({
                    "msg": "未找到用户",
                }, ensure_ascii=False, status=401)

    async def post(self, request, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }, ensure_ascii=False, status=401)

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }, ensure_ascii=False, status=500)
        else:
            if u:
                insert = request.json
                try:
                    validate(instance=insert, schema=Todo_Schema)
                except Exception as e:
                    return jsonify({
                        "msg": "参数错误",
                        "error": str(e)
                    }, ensure_ascii=False, status=401)
                else:
                    Todo.get(uid).append(insert)
                    return jsonify({
                        "msg": "插入成功"
                    }, ensure_ascii=False)
            else:
                return jsonify({
                    "msg": "未找到用户",
                }, ensure_ascii=False, status=401)


todo_view = TodoAPI.as_view()
api_todo.add_route(todo_view, '/todo/<uid:int>')

api_v1 = Blueprint.group(api_user, api_todo)

app.blueprint(api_v1, url_prefix='/v1')

if __name__ == "__main__":
    app.run(host='localhost', port=5000)
