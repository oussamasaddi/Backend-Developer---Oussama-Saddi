import unittest
from flask import Flask, jsonify
from flask.testing import FlaskClient
from app import app

#test case 

class FlaskTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        
        cls.client = app.test_client()

    def test_get_product_by_id_valid(self):
        
        
        response = self.client.get('/products/getbyid/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['title'], 'Essence Mascara Lash Princess')
        self.assertEqual(response.json['price'], 9.99)
    def test_rate_limiting(self):
        
        for _ in range(199):
            response = self.client.get('/products/getbyid/1')
            self.assertEqual(response.status_code, 200)

        # Test exceeding the rate limit
        response = self.client.get('/products/getbyid/1')
        self.assertEqual(response.status_code, 429)
        
   

if __name__ == '__main__':
    unittest.main()