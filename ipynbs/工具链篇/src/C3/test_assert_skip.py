import unittest
class demoTest(unittest.TestCase):
    @unittest.skip("跳过")
    def test_eq(self):
        self.assertEqual(4 + 5,9)
    @unittest.expectedFailure 
    def test_not_eq(self):
        self.assertNotEqual(5 * 2,10)
    @unittest.skipIf(1==0, "if 1 ==0")
    def test_seq(self):
        a=["1","2","3"]
        b = ("1","2","3")
        self.assertSequenceEqual(a, b)
    @unittest.skipUnless(1==0, "unless 1 ==0")
    def test_seq_2(self):
        a=["1","2","3"]
        b = ("1","2","3")
        self.assertSequenceEqual(a, b)
    @unittest.expectedFailure 
    def test_not_seq(self):
        a = ["1","2","3"]
        b = ("1","2","3","4")
        self.assertSequenceEqual(a, b)