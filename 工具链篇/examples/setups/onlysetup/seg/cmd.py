import argparse
import jieba
from .seg import seg
from .version import __version__


def cmdseg() -> None:
    jieba.setLogLevel("INFO")
    parser = argparse.ArgumentParser(prog="seg")
    parser.add_argument("msg", type=str, help="要重复的消息", default="")
    parser.add_argument("-v", "--version", help=u"查看版本号", action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()
    seg_list = seg(args.msg)
    print(", ".join(seg_list))
