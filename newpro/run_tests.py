import unittest
import sys
import os

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import test modules
from test_catalog_service import TestCatalogService
from test_order_service import TestOrderService
from test_frontend_service import TestFrontendService

# Create test suite
def create_test_suite():
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add unit tests
    test_suite.addTest(unittest.makeSuite(TestCatalogService))
    test_suite.addTest(unittest.makeSuite(TestOrderService))
    test_suite.addTest(unittest.makeSuite(TestFrontendService))
    
    return test_suite

if __name__ == '__main__':
    # Create test suite
    suite = create_test_suite()
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return non-zero exit code if tests failed
    sys.exit(not result.wasSuccessful())