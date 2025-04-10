import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path to import the frontend_service module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the frontend service module
import frontend_service
from frontend_service import app


class TestFrontendService(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True
        
        # Sample book data for testing
        self.test_books_by_topic = {
            "items": {
                "Test Book 1": 1,
                "Test Book 2": 2
            }
        }
        
        self.test_book_info = {
            "item_number": 1,
            "title": "Test Book 1",
            "topic": "test topic",
            "stock": 10,
            "cost": 30
        }
        
        self.test_purchase_response = {
            "success": True,
            "message": "Purchase successful",
            "order": {
                "order_id": "test-order-id",
                "item_number": "1",
                "timestamp": "2023-01-01 12:00:00"
            }
        }
    
    @patch('frontend_service.requests.get')
    def test_search(self, mock_get):
        # Mock the GET response from catalog service
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.test_books_by_topic
        mock_get.return_value = mock_response
        
        # Test search endpoint
        response = self.app.get('/search/test topic')
        data = json.loads(response.data)
        
        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Check response data
        self.assertEqual(data, self.test_books_by_topic)
        
        # Verify that the catalog service was called correctly
        mock_get.assert_called_once_with('http://localhost:5001/query/subject/test topic')
        
        # Test search with catalog service error
        mock_response.status_code = 500
        response = self.app.get('/search/test topic')
        data = json.loads(response.data)
        
        # Check response status code
        self.assertEqual(response.status_code, 500)
        
        # Check response data
        self.assertEqual(data['error'], 'Failed to search books')
    
    @patch('frontend_service.requests.get')
    def test_info(self, mock_get):
        # Mock the GET response from catalog service
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.test_book_info
        mock_get.return_value = mock_response
        
        # Test info endpoint
        response = self.app.get('/info/1')
        data = json.loads(response.data)
        
        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Check response data
        self.assertEqual(data, self.test_book_info)
        
        # Verify that the catalog service was called correctly
        mock_get.assert_called_once_with('http://localhost:5001/query/item/1')
        
        # Test info with catalog service error
        mock_response.status_code = 404
        response = self.app.get('/info/999')
        data = json.loads(response.data)
        
        # Check response status code
        self.assertEqual(response.status_code, 404)
        
        # Check response data
        self.assertEqual(data['error'], 'Book not found')
    
    @patch('frontend_service.requests.post')
    def test_purchase(self, mock_post):
        # Mock the POST response from order service
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.test_purchase_response
        mock_post.return_value = mock_response
        
        # Test purchase endpoint
        response = self.app.post('/purchase/1')
        data = json.loads(response.data)
        
        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Check response data
        self.assertEqual(data, self.test_purchase_response)
        
        # Verify that the order service was called correctly
        mock_post.assert_called_once_with('http://localhost:5002/purchase/1')
        
        # Test purchase with order service error
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Book is out of stock"}
        response = self.app.post('/purchase/2')
        data = json.loads(response.data)
        
        # Check response status code
        self.assertEqual(response.status_code, 400)
        
        # Check response data
        self.assertEqual(data['error'], 'Book is out of stock')


if __name__ == '__main__':
    unittest.main()