import unittest
class demoTest(unittest.TestCase):
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

    def test_almost_eq(self):
        self.assertAlmostEqual(1.003, 1.004, places = 2)

    def test_not_almost_eq(self):
        self.assertAlmostEqual(1.003, 1.004, places = 4)
        
    def test_exc(self):
        def fun():
            assert 0
        self.assertRaises(AssertionError, fun)

    def test_with_exc(self):
        def fun():
            assert 0
        with self.assertRaises(AssertionError) as a:
            fun()
