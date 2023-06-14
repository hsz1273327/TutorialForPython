#!/usr/bin/env python
# coding:utf-8 
u"""
Usage: 
  test1.py [option] <num>...
  test1.py (-v|--version)
  test1.py (-a|--all)
  test1.py (-h|--help)
  

Options:
  -h --help      帮助
  -v --version   显示版本号.
  -a --all       显示全部参数
"""

from docopt import docopt
from math import sqrt
__version__="0.1.0"



def version():
    return "version:"+__version__

def main():
    args = docopt(__doc__)
    
    if args.get("-h") or args.get("-help"):
        print(__doc__)
    elif args.get("-v") or args.get("--version"):
        print(__version__)
    elif args.get("-a") or args.get("--all"):
        print(args)
    elif args.get("<num>"):
        print(" ".join(map(lambda x :str(sqrt(float(x))),args.get("<num>"))))
    else:
        print("wrong args!")
        print(__doc__)



if __name__ == '__main__':
    main()
