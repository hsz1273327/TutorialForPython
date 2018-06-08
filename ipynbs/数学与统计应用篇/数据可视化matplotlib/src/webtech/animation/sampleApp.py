# coding:utf-8
from flask import Flask, request
app = Flask(__name__)

from rain import rain




@app.route("/rain",methods=['GET'])
def rain_video():
    video = rain()
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
