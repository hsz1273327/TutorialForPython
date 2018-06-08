from __future__ import absolute_import
from flask import Blueprint
main = Blueprint('main', __name__)
from . import view
