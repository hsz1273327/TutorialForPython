#!/usr/bin/env python3
import argparse
from math import sqrt
from gooey import Gooey, GooeyParser


__version__="0.1.0"

def sqrtarg(number):
    return sqrt(number)

def version():
    return "version:"+__version__
@Gooey(language='chinese')
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int, help=u"求开根的参数")
    parser.add_argument("-v","--version", help=u"查看版本号",action="store_true")

    args = parser.parse_args()
    
    if args.version:
        print(version())
    if args.number:
        print(sqrtarg(args.number))

if __name__ == '__main__':
    main()
