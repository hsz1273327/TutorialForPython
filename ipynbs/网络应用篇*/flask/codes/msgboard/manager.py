#--*--coding:utf-8 --*--
from __future__ import absolute_import,division,print_function,unicode_literals
"""
A startup manager of the application.

Author:Huang Sizhe
Date:22/01/2016
License:MIT
======================================

应用的启动文件

作者:黄思喆
日期:2016年1月22日
本应用使用MIT许可证

"""

__author__ = "Huang Sizhe"
__date__ = "22/01/2016"

import os
import sys


root = os.path.dirname(__file__)

from app import creat_app,db
from app.model import Message,User,Role

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager,Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def init_db(db):
    db.create_all()
    admin_role = Role(name='Admin')
    mod_role = Role(name='Moderator')
    user_role = Role(name='User')
    db.session.add_all([admin_role, mod_role, user_role])
    for i in AdminAccount:
        adminaccount = User(name=i["name"] ,email=i["email"],role =admin_role ,password = i["password"])
        db.session.add(adminaccount)
    db.session.commit()
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)

def make_shell_context():
    return dict(app=app,
                db=db,
                Message=Message,
                User=User,
                Role=Role,
                init_db=init_db)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()
