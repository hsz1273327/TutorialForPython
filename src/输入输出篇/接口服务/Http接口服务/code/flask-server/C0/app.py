from flask import Flask, jsonify, request
from flask.views import MethodView
from jsonschema import validate
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

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

    def get(self):
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


user_index_view = UserIndexAPI.as_view('user_index_api')
user_view = UserAPI.as_view('user_api')


app.add_url_rule('/user', view_func=user_index_view)
app.add_url_rule('/user/<int:uid>', view_func=user_view)

if __name__ == "__main__":
    app.run()
