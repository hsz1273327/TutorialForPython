#--*--coding:utf-8 --*--
from __future__ import absolute_import,division,print_function,unicode_literals

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string' 
    BCRYPT_LEVEL = 10 # 配置Flask-Bcrypt拓展
    @staticmethod
    def init_app(app):
        pass
    

class DevelopmentConfig(Config): 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    DEBUG = True
         
class TestingConfig(Config): 
    TESTING = True
    
class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig, 
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

AdminAccount = [{"name":"hsz",
                 "email":"hsz1273327@sina.cn",
                 "password":"hsz881224"
        }] 

BASE_URL = "127.0.0.1:5000"