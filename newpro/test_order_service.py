import unittest
import json
import os
import sys
import csv
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path to import the order_service module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the order service module
import order_service
from order_service import app


class TestOrderService(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True
        
        # Sample book data for testing
        self.test_book = {
            "item_number": 1,
            "title": "Test Book 1",
            "topic": "test topic",
            "stock": 10,
            "cost": 30
        }
        
        # Sample out-of-stock book
        self.out_of_stock_book = {
            "item_number": 2,
            "title": "Test Book 2",
            "topic": "test topic",
            "stock": 0,
            "cost": 25
        }
    
    @patch('order_service.requests.get')
    @patch('order_service.requests.put')
    @patch('order_service.write_order')
    def test_purchase_success(self, mock_write_order, mock_put, mock_get):
        # Mock the GET response from catalog service
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = self.test_book
        mock_get.return_value = mock_get_response
        
        # Mock the PUT response from catalog service
        mock_put_response = MagicMock()
        mock_put_response.status_code = 200
        mock_put_response.json.return_value = {"success": True, "message": "Book updated successfully"}
        mock_put.return_value = mock_put_response
        
        # Test purchase endpoint
        response = self.app.post('/purchase/1')
        data = json.loads(response.data)
        
        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Check response data
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Purchase successful')
        self.assertIn('order', data)
        self.assertIn('order_id', data['order'])
        self.assertEqual(data['order']['item_number'], '1')
        
        # Verify that the catalog service was called correctly
        mock_get.assert_called_once_with('http://localhost:5001/query/item/1')
        mock_put.assert_called_once()
        
        # Verify that the stock was decremented by 1
        put_args, put_kwargs = mock_put.call_args
        self.assertEqual(put_args[0], 'http://localhost:5001/update/1')
        self.assertEqual(put_kwargs['json'], {"stock": 9})
        
        # Verify that write_order was called
        mock_write_order.assert_called_once()
    
    @patch('order_service.requests.get')
    @patch('order_service.requests.put')
    @patch('order_service.write_order')
    def test_purchase_out_of_stock(self, mock_write_order, mock_put, mock_get):
        # Mock the GET response from catalog service
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = self.out_of_stock_book
        mock_get.return_value = mock_get_response
        
        # Test purchase endpoint with out-of-stock book
        response = self.app.post('/purchase/2')
        data = json.loads(response.data)
        
        # Check response status code
        self.assertEqual(response.status_code, 400)
        
        # Check response data
        self.assertEqual(data['error'], 'Book is out of stock')
        
        # Verify that the catalog service GET was called
        mock_get.assert_called_once_with('http://localhost:5001/query/item/2')
        
        # Verify that the catalog service PUT was not called
        mock_put.assert_not_called()
        
        # Verify that write_order was not called
        mock_write_order.assert_not_called()
    
    @patch('order_service.requests.get')
    def test_purchase_book_not_found(self, mock_get):
        # Mock the GET response from catalog service
        mock_get_response = MagicMock()
        mock_get_response.status_code = 404
        mock_get.return_value = mock_get_response
        
        # Test purchase endpoint with non-existent book
        response = self.app.post('/purchase/999')
        data = json.loads(response.data)
        
        # Check response status code
        self.assertEqual(response.status_code, 500)
        
        # Check response data
        self.assertEqual(data['error'], 'Failed to retrieve book information')
        
        # Verify that the catalog service GET was called
        mock_get.assert_called_once_with('http://localhost:5001/query/item/999')
    
    @patch('order_service.requests.get')
    @patch('order_service.requests.put')
    def test_purchase_update_failure(self, mock_put, mock_get):
        # Mock the GET response from catalog service
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = self.test_book
        mock_get.return_value = mock_get_response
        
        # Mock the PUT response from catalog service (failure)
        mock_put_response = MagicMock()
        mock_put_response.status_code = 500
        mock_put.return_value = mock_put_response
        
        # Test purchase endpoint with update failure
        response = self.app.post('/purchase/1')
        data = json.loads(response.data)
        
        # Check response status code
        self.assertEqual(response.status_code, 500)
        
        # Check response data
        self.assertEqual(data['error'], 'Failed to update book stock')


if __name__ == '__main__':
    unittest.main()