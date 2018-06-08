from flask import Flask
from flask_mail import Mail,Message

app = Flask(__name__)
mail = Mail(app)

app.config.from_pyfile("config.py")

msg = Message(subject="来自SMTP的问候……",html="""<html><body><h1>Hello</h1>
                            <p>send by <a href="http://www.python.org">Python</a>...</p>
                            </body></html>""",
                  sender=("Python开发者HUANG", "15851390734@163.com"),
                  recipients=[("我的朋友","469389377@qq.com")])