#--*--coding:utf-8 --*--
from __future__ import absolute_import,division,print_function,unicode_literals

__author__ = "Huang Sizhe"
__date__ = "22/01/2016"

import os
import sys
from flask.ext.script import Manager,Shell

root = os.path.dirname(__file__)
#把新加的表名放进去便于操作
from app import app,msg,mail

manager = Manager(app)

def make_shell_context():
    return dict(app=app,msg=msg,mail=mail)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()