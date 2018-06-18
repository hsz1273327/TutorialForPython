#--*--coding:utf-8 --*--
from __future__ import absolute_import,division,print_function,unicode_literals
"""
A message board appliation.

Author:Huang Sizhe
Date:22/01/2016
License:MIT
======================================

留言板应用

作者:黄思喆
日期:2016年1月22日
本应用使用MIT许可证

"""
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment

from config import config

bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
