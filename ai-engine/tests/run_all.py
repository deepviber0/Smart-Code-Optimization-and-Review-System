import unittest
import sys
import os

if __name__ == '__main__':
    # Add parent directory to sys.path to allow importing ai-engine modules
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
