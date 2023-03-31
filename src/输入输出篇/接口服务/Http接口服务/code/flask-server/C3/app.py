from flask import Flask, Blueprint, jsonify, request, after_this_request
from flask.views import MethodView
from jsonschema import validate
from functools import wraps
import time

def print_time(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start = time.time()
        response = f(*args, **kwargs)
        end = time.time()
        spend = end-start
        print(f"spend {spend} s")
        return response
    return decorated_function
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api_v1 = Blueprint('v1', __name__)


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


class UserIndexAPI(MethodView):
    decorators = [print_time]
    def get(self):
        @after_this_request
        def _after_this_request(response):
            print("after_this_request")
            return response
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

        return jsonify(result)

    def post(self):
        insert = request.json

        try:
            validate(instance=insert, schema=User_Schema)
        except Exception as e:
            return jsonify({
                "msg": "参数错误",
                "error": str(e)
            }), 401
        else:
            uid = User.append(insert)
            return jsonify({
                "msg": "插入成功",
                "uid": uid
            })


class UserAPI(MethodView):

    def get(self, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }), 401

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }), 500
        else:
            if u:
                return jsonify(u)
            else:
                return jsonify({
                    "msg": "未找到用户",
                }), 401

    def put(self, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }), 401

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }), 500
        else:
            if u:
                insert = request.json
                u.update(insert)
                return jsonify({
                    "msg": "更新成功"
                })
            else:
                return jsonify({
                    "msg": "未找到用户",
                }), 401

    def delete(self, uid):
        try:
            u = User[uid]
        except IndexError as dn:
            return jsonify({
                "msg": "未找到用户",
            }), 401

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }), 500
        else:
            if u:
                User[uid] = None
                return jsonify({
                    "msg": "删除成功",
                })
            else:
                return jsonify({
                    "msg": "未找到用户",
                }), 401


@app.before_first_request
def _before_first_request():
    print("before_first_request")


@app.before_request
def _before_request():
    print("before_request")


@app.after_request
def _after_request(response):
    print(f"after_request:{response}")
    return response


@app.teardown_request
def _teardown_request(response):
    print(f"teardown_request:{response}")
    return response


@api_v1.before_request
def _bp_before_request():
    print("bp_before_request")


@api_v1.teardown_request
def _bp_teardown_request(response):
    print(f"bp_teardown_request:{response}")
    return response


@api_v1.after_request
def _bp_after_request(response):
    print(f"bp_after_request:{response}")
    return response


user_index_view = UserIndexAPI.as_view('user_index_api')
user_view = UserAPI.as_view('user_api')


api_v1.add_url_rule('/user', view_func=user_index_view)
api_v1.add_url_rule('/user/<int:uid>', view_func=user_view)

app.register_blueprint(api_v1, url_prefix='/v1')

if __name__ == "__main__":
    app.run()
