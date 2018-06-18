from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config.from_pyfile('config.py')
mail = Mail(app)

from flask_mail import Message

from config import ADMINS

@app.route("/")
def index():
    msg = Message("Hello",
                  sender=ADMINS[0],
                  recipients=["469389377@qq.com"])
    msg.body = 'text body'
    msg.html = '<b>HTML</b>'
    mail.send(msg)
    return "send"
if __name__ == '__main__':
    app.run()
