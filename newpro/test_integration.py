import unittest
import json
import os
import sys
import requests
import time
import subprocess
import signal
import atexit
from unittest.mock import patch

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # URLs for the services
        cls.frontend_url = 'http://localhost:5000'
        cls.catalog_url = 'http://localhost:5001'
        cls.order_url = 'http://localhost:5002'
        
        # Check if services are already running
        try:
            # Check if frontend service is running
            response = requests.get(f'{cls.frontend_url}/')
            cls.frontend_running = response.status_code == 200
        except requests.exceptions.ConnectionError:
            cls.frontend_running = False
            
        try:
            # Check if catalog service is running
            response = requests.get(f'{cls.catalog_url}/query/subject/distributed systems')
            cls.catalog_running = response.status_code == 200
        except requests.exceptions.ConnectionError:
            cls.catalog_running = False
            
        try:
            # Check if order service is running
            # Just try to connect, we don't expect a 200 for a GET on this endpoint
            requests.get(f'{cls.order_url}/purchase/1')
            cls.order_running = True
        except requests.exceptions.ConnectionError:
            cls.order_running = False
        
        # Start services if not running
        cls.processes = []
        
        if not cls.catalog_running:
            print("Starting catalog service...")
            catalog_process = subprocess.Popen(
                [sys.executable, 'catalog_service.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            cls.processes.append(catalog_process)
            time.sleep(2)  # Wait for service to start
        
        if not cls.order_running:
            print("Starting order service...")
            order_process = subprocess.Popen(
                [sys.executable, 'order_service.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            cls.processes.append(order_process)
            time.sleep(2)  # Wait for service to start
        
        if not cls.frontend_running:
            print("Starting frontend service...")
            frontend_process = subprocess.Popen(
                [sys.executable, 'frontend_service.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            cls.processes.append(frontend_process)
            time.sleep(2)  # Wait for service to start
        
        # Register cleanup function
        atexit.register(cls.tearDownClass)
    
    @classmethod
    def tearDownClass(cls):
        # Stop any processes we started
        for process in cls.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                # Force kill if terminate doesn't work
                if sys.platform == 'win32':
                    os.kill(process.pid, signal.CTRL_C_EVENT)
                else:
                    os.kill(process.pid, signal.SIGKILL)
    
    def test_search_books(self):
        """Test searching for books by topic through the frontend service"""
        response = requests.get(f'{self.frontend_url}/search/distributed systems')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify response structure
        self.assertIn('items', data)
        self.assertTrue(len(data['items']) > 0)
        
        # Verify specific books are found
        book_titles = data['items'].keys()
        self.assertTrue(any('DOS' in title for title in book_titles))
        self.assertTrue(any('RPC' in title for title in book_titles))
    
    def test_get_book_info(self):
        """Test getting detailed book information through the frontend service"""
        # First search for books to get an item number
        search_response = requests.get(f'{self.frontend_url}/search/distributed systems')
        search_data = search_response.json()
        
        # Get the first book's item number
        first_book_title = list(search_data['items'].keys())[0]
        item_number = search_data['items'][first_book_title]
        
        # Get book info
        info_response = requests.get(f'{self.frontend_url}/info/{item_number}')
        self.assertEqual(info_response.status_code, 200)
        info_data = info_response.json()
        
        # Verify book info
        self.assertEqual(info_data['item_number'], item_number)
        self.assertEqual(info_data['title'], first_book_title)
        self.assertIn('stock', info_data)
        self.assertIn('cost', info_data)
    
    def test_purchase_flow(self):
        """Test the complete purchase flow through all services"""
        # First get a book that's in stock
        info_response = requests.get(f'{self.frontend_url}/info/1')
        info_data = info_response.json()
        
        # Record initial stock
        initial_stock = info_data['stock']
        
        # Only proceed if book is in stock
        if initial_stock > 0:
            # Purchase the book
            purchase_response = requests.post(f'{self.frontend_url}/purchase/1')
            self.assertEqual(purchase_response.status_code, 200)
            purchase_data = purchase_response.json()
            
            # Verify purchase was successful
            self.assertTrue(purchase_data['success'])
            self.assertEqual(purchase_data['message'], 'Purchase successful')
            self.assertIn('order', purchase_data)
            self.assertIn('order_id', purchase_data['order'])
            
            # Verify stock was decremented
            updated_info_response = requests.get(f'{self.frontend_url}/info/1')
            updated_info_data = updated_info_response.json()
            self.assertEqual(updated_info_data['stock'], initial_stock - 1)
        else:
            self.skipTest("Book is out of stock, skipping purchase test")
    
    def test_out_of_stock_handling(self):
        """Test handling of out-of-stock books"""
        # First get a book's current stock
        info_response = requests.get(f'{self.frontend_url}/info/1')
        info_data = info_response.json()
        
        # If book is already out of stock, we can test directly
        if info_data['stock'] == 0:
            purchase_response = requests.post(f'{self.frontend_url}/purchase/1')
            self.assertEqual(purchase_response.status_code, 400)
            purchase_data = purchase_response.json()
            self.assertEqual(purchase_data['error'], 'Book is out of stock')
        else:
            # We need to update the stock to 0 first
            update_response = requests.put(
                f'{self.catalog_url}/update/1',
                json={"stock": 0},
                headers={"Content-Type": "application/json"}
            )
            self.assertEqual(update_response.status_code, 200)
            
            # Now try to purchase
            purchase_response = requests.post(f'{self.frontend_url}/purchase/1')
            self.assertEqual(purchase_response.status_code, 400)
            purchase_data = purchase_response.json()
            self.assertEqual(purchase_data['error'], 'Book is out of stock')
            
            # Restore original stock
            restore_response = requests.put(
                f'{self.catalog_url}/update/1',
                json={"stock": info_data['stock']},
                headers={"Content-Type": "application/json"}
            )
            self.assertEqual(restore_response.status_code, 200)


if __name__ == '__main__':
    unittest.main()