#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import argparse
from math import sqrt
__version__="0.1.0"

def sqrtarg(number):
    return sqrt(number)

def version():
    return "version:"+__version__

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int, help=u"求开根的参数")
    parser.add_argument("-v","--version", help=u"查看版本号",action="version",version=__version__)
    args = parser.parse_args()
    if args.number:
        print(sqrtarg(args.number))

if __name__ == '__main__':
    main()
