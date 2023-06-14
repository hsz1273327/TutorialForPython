import jieba

from typing import Literal

SegMode = Literal["full", "precision", "search"]


def seg(msg: str, mode: SegMode = "precision") -> list[str]:
    match mode:
        case "search":
            seg_list = jieba.lcut_for_search(msg)
        case "full":
            seg_list = jieba.lcut(msg, cut_all=True)
        case _:
            seg_list = jieba.lcut(msg)
    return seg_list
