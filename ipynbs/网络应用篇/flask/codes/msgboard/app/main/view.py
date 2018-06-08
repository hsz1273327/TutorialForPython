#--*--coding:utf-8 --*--
from __future__ import absolute_import,division,print_function,unicode_literals

from flask import render_template,make_response,redirect,url_for,flash,request


from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/',methods = ["GET","POST"])
def index():
    return render_template('main/index.html', form=form)
