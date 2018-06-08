# coding:utf-8
from flask import Flask, request
app = Flask(__name__)

from tools import draw_k_svg




@app.route("/k-line",methods=['GET'])
def k_line():
    id_str = request.args.get('id')
    from_date_str = request.args.get('from_date')
    to_date_str =  request.args.get('to_date')

    svg = draw_k_svg(id_str,from_date_str,to_date_str)
    return """<!DOCTYPE html>
    <html>
    <head>
    <meta name="generator" content="dazhes2.2.1" />
    <meta name="copyright" content="dazhes Inc. All Rights Reserved" />
    <meta name="alexaVerifyID" content="ozj_7kkagDQEWjPWlaOukthxUGY" />
    <title> svg test</title>
    </head>
    <body>{svg}</body>
    </html>""".format(svg=svg)


if __name__ == "__main__":
    app.run()
