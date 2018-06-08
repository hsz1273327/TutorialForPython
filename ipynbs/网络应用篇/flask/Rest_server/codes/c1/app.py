# --*-- coding:utf-8 --*--
from __future__ import print_function, unicode_literals, division

from flask import Flask,jsonify
from flask.views import MethodView

app = Flask(__name__)

class HelloAPI(MethodView):
    
    def get(self):
        return jsonify({"result":"hello!"})
        

app.add_url_rule('/hello/',view_func=HelloAPI.as_view('hello'.encode("utf-8")))

if __name__ == '__main__':
    app.run(debug=True)