from app import app
import unittest

class SanicTestCase(unittest.TestCase):

    def setUp(self):
        print("测试开始")
        self.app = app.test_client
    def tearDown(self):
        print("测试结束")

    def test_user(self):
        request, response  = self.app.get('/v1/user')
        assert "user-count" in response.json.keys()