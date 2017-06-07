
import unittest
    
from func_oper_unitest import multiply,summing

class Test_mul(unittest.TestCase):
    def setUp(self):
        pass
    def test_number_3_4(self):
        self.assertEqual(multiply(3,4),12)
    def test_string_a_3(self):
        self.assertEqual(multiply('a',3),'aaa')
        
class Test_sum(unittest.TestCase):
    def setUp(self):
        pass
    def test_number_3_4(self):
        self.assertEqual(summing(3,4),7)
    def test_number_3_4_5(self):
        self.assertEqual(summing(3,4,5),12)
class TestCase1(unittest.TestCase):
    def setUp(self):
        pass
    def test_sum_mul_2_3_mul_2_3(self):
        self.assertEqual(summing(multiply(2,3),multiply(2,3)),12)

if __name__ == '__main__':
    unittest.main()