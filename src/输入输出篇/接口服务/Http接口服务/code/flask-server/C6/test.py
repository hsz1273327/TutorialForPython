import json
import unittest
import app
class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        print("测试开始")
        self.app = app.app.test_client()
    def tearDown(self):
        print("测试结束")

    def test_user(self):
        rv = self.app.get('/v1/user')
        assert "user-count" in json.loads(rv.data).keys()