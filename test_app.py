import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_hello_xss_escaped(self):
        response = self.client.get('/hello?name=<script>alert(1)</script>')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'<script>', response.data)

if __name__ == '__main__':
    unittest.main()
