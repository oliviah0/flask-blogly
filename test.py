from unittest import TestCase
from app import app

class FlaskTest(TestCase):
    """Tests if the routing works"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_users(self):
        """Tests the index"""

        with self.client:
            response = self.client.get('/users')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<ul>', response.data)
            self.assertIn(b'<h1> Users </h1>', response.data)
    
    def test_user(self):

        with self.client:
            response = self.client.get('/users/user/2')
            self.assertEqual(response.status_code, 200)
    
    def test_create(self):

        with self.client:
            response = self.client.get('/users/create')
            self.assertEqual(response.status_code, 200)


    def test_edit(self):

        with self.client:
            response = self.client.get('/users/user/2/edit')
            self.assertEqual(response.status_code, 200)

    

  

