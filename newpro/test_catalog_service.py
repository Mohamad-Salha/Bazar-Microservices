import unittest
import json
import os
import sys
import csv
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path to import the catalog_service module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the catalog service module
import catalog_service
from catalog_service import app


class TestCatalogService(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True
        
        # Create a temporary test books file
        self.test_books = [
            {"item_number": 1, "title": "Test Book 1", "topic": "test topic", "stock": 10, "cost": 30},
            {"item_number": 2, "title": "Test Book 2", "topic": "test topic", "stock": 5, "cost": 25},
            {"item_number": 3, "title": "Test Book 3", "topic": "another topic", "stock": 15, "cost": 20}
        ]
    
    @patch('catalog_service.read_books')
    def test_query_by_subject(self, mock_read_books):
        # Mock the read_books function to return test data
        mock_read_books.return_value = self.test_books
        
        # Test querying by subject
        response = self.app.get('/query/subject/test topic')
        data = json.loads(response.data)
        
        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Check response data
        self.assertIn('items', data)
        self.assertEqual(len(data['items']), 2)  # Should find 2 books with 'test topic'
        self.assertIn('Test Book 1', data['items'])
        self.assertIn('Test Book 2', data['items'])
        
        # Test querying by non-existent subject
        response = self.app.get('/query/subject/nonexistent')
        data = json.loads(response.data)
        
        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Check response data - should be empty
        self.assertIn('items', data)
        self.assertEqual(len(data['items']), 0)
    
    @patch('catalog_service.read_books')
    def test_query_by_item(self, mock_read_books):
        # Mock the read_books function to return test data
        mock_read_books.return_value = self.test_books
        
        # Test querying by item number
        response = self.app.get('/query/item/1')
        data = json.loads(response.data)
        
        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Check response data
        self.assertEqual(data['item_number'], 1)
        self.assertEqual(data['title'], 'Test Book 1')
        self.assertEqual(data['topic'], 'test topic')
        self.assertEqual(data['stock'], 10)
        self.assertEqual(data['cost'], 30)
        
        # Test querying by non-existent item number
        response = self.app.get('/query/item/999')
        
        # Check response status code
        self.assertEqual(response.status_code, 404)
    
    @patch('catalog_service.read_books')
    @patch('catalog_service.write_books')
    def test_update_item(self, mock_write_books, mock_read_books):
        # Mock the read_books function to return test data
        mock_read_books.return_value = self.test_books
        
        # Test updating stock
        response = self.app.put('/update/1', 
                              json={"stock": 5},
                              content_type='application/json')
        data = json.loads(response.data)
        
        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Check that write_books was called
        mock_write_books.assert_called_once()
        
        # Check that the stock was updated in the test_books list
        updated_books = mock_write_books.call_args[0][0]
        updated_book = next(book for book in updated_books if book['item_number'] == 1)
        self.assertEqual(updated_book['stock'], 5)
        
        # Test updating non-existent item
        mock_write_books.reset_mock()
        response = self.app.put('/update/999', 
                              json={"stock": 5},
                              content_type='application/json')
        
        # Check response status code
        self.assertEqual(response.status_code, 404)
        
        # Check that write_books was not called
        mock_write_books.assert_not_called()


if __name__ == '__main__':
    unittest.main()