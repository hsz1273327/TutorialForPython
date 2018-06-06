
import unittest
    
from func_oper_unitest import multiply,summing

def setUpModule():
    print("setUpModule")
def tearDownModule(): 
    print("tearUpModule")

    
class Test_mul(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")
    def setUp(self):
        print("instance setUp")
    def tearDown(self):
        print("instance tearDown")
    def test_number_3_4(self):
        print("t1")
        self.assertEqual(multiply(3,4),12)
    def test_string_a_3(self):
        print("t2")
        self.assertEqual(multiply('a',3),'aaa')
        
        


if __name__ == '__main__':
    unittest.main()