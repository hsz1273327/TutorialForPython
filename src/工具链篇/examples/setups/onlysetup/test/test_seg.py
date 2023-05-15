import unittest

from seg import seg


class Test_seg(unittest.TestCase):

    def test_seg_precision(self) -> None:
        self.assertListEqual(
            seg('我来到北京清华大学'),
            ["我", "来到", "北京", "清华大学"])

    def test_seg_full(self) -> None:
        self.assertListEqual(
            seg('我来到北京清华大学', "full"),
            ["我", "来到", "北京", "清华", "清华大学", "华大", "大学"])

    def test_seg_search(self) -> None:
        self.assertListEqual(
            seg("小明硕士毕业于中国科学院计算所,后在日本京都大学深造", "search"),
            ["小明", "硕士", "毕业", "于", "中国", "科学", "学院", "科学院", "中国科学院", "计算", "计算所", ",", "后", "在", "日本", "京都", "大学", "日本京都大学", "深造"])

# if __name__ == '__main__':
#     unittest.main()
