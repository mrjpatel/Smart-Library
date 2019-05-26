from flask_main import app
import unittest

# python -m unittest test_app


class TestMyApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_main(self):
        rv = self.app.get('/')
        assert rv.status == '200 OK'
        # assert False
