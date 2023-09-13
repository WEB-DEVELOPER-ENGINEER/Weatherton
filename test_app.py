import unittest
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home_page_redirect(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)

    def test_weather_page(self):
        response = self.app.get('/weather/NewYork/NY')
        self.assertEqual(response.status_code, 200)

    def test_error_page(self):
        response = self.app.get('/nonexistentpage')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()

