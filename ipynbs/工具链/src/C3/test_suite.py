import unittest
class ArithTest(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(4 + 5,9)

    def test_not_eq(self):
        self.assertNotEqual(5 * 2,10)

    def test_seq(self):
        a=["1","2","3"]
        b = ("1","2","3")
        self.assertSequenceEqual(a, b)

    def test_not_seq(self):
        a = ["1","2","3"]
        b = ("1","2","3","4")
        self.assertSequenceEqual(a, b)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(ArithTest("test_eq"))
    suite.addTest(ArithTest('test_seq'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = suite()
    runner.run(test_suite)