from flask import Flask,render_template,url_for,flash,redirect
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap


from flask.ext.wtf import Form
from wtforms import RadioField, SubmitField 
from wtforms.validators import Required
  
import time
from datetime import timedelta, timezone,datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'# 新增
app.debug = True
bootstrap = Bootstrap(app)
manager = Manager(app)

#新增
class TimeForm(Form):
    country = RadioField("Which country? ", 
                      choices=[('Japan', 'Japan'), ('UK', 'UK'), ('France', 'France'),("Australia","Australia")],
                      validators=[Required()])
    submit = SubmitField('Submit')

@app.template_filter('changeTime')
def changeTime(text):
    now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
    return str(now_utc.astimezone(timezone(timedelta(hours=text))).strftime('%a, %b %d %H:%M'))    


@app.route('/',methods = ["POST","GET"])
def worldtime():
    timezones = {
        "China":(8,u"北京"),
        "Japan":(9,u"东京"),
        "UK":(0,u"伦敦"),
        "France":(2,u"巴黎"),
        "Australia":(10,u"悉尼")
    }
    chinatimezone,chinacity = timezones.get("China")
    timezone = chinatimezone
    city = chinacity
    timeform = TimeForm()
    if timeform.validate_on_submit():
        country = timeform.country.data
        if country:
            country = str(timeform.country.data)
            timezone,city = timezones.get(country)
        else:
            flash("Looks like there is something wrong!")
            return redirect(url_for('worldtime'))   
    
        
    return render_template('myapp/index.html',timeform=timeform,
                           chinacity = chinacity,
                           chinatime=chinatimezone,
                           city= city, 
                           timezone=timezone)