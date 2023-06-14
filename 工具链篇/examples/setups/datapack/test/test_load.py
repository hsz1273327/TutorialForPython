import unittest
import pkgutil


class Test_load(unittest.TestCase):

    def test_load(self) -> None:
        test_data = pkgutil.get_data('simpledatapack', 'test.txt')
        self.assertEqual(test_data, b"this is a test.")
