import unittest
class demoTest(unittest.TestCase):
   
    def test_subtest(self):
        for i in range(0, 6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)