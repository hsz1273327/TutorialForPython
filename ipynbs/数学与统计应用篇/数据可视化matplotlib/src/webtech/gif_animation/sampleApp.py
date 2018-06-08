# coding:utf-8
from flask import Flask, request
app = Flask(__name__)

from double_pendulum import double_pendulum




@app.route("/double_pendulum",methods=['GET'])
def double_pendulum_video():
    video = double_pendulum()
    return """<!DOCTYPE html>
    <html>
    <head>
    <meta name="generator" content="dazhes2.2.1" />
    <meta name="copyright" content="dazhes Inc. All Rights Reserved" />
    <meta name="alexaVerifyID" content="ozj_7kkagDQEWjPWlaOukthxUGY" />
    <title> svg test</title>
    </head>
    <body>{video}</body>
    </html>""".format(video=video)


if __name__ == "__main__":
    app.run()
