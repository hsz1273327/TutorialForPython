from flask import Flask
from flask.ext.mail import Mail 

app = Flask(__name__)
app.debug = True
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.163.com' 
#app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_USERNAME'] = "hsz"
app.config['MAIL_PASSWORD'] = 'hsz881224'


@app.route('/')
def hello():
    return "Hello, world! - Flask"

if __name__ == '__main__':
    app.run()