#coding:UTF-8
import os
import sys

root = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(root, 'site-packages'))

from firstappplus import manager

if __name__ == '__main__':
    manager.run()