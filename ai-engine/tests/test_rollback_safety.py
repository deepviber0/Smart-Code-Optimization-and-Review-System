import unittest
import os
import sys

# Ensure imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimizer import optimize_code

class TestRollbackSafety(unittest.TestCase):
    def setUp(self):
        self.samples_dir = os.path.join(os.path.dirname(__file__), 'samples')
        with open(os.path.join(self.samples_dir, 'js', 'malformed.js'), 'r', encoding='utf-8') as f:
            self.malformed_js = f.read()

    def test_malformed_braces(self):
        """Test that syntax errors trigger an immediate rollback to original code."""
        result = optimize_code(self.malformed_js, 'javascript', [])
        self.assertEqual(result['code'], self.malformed_js, "Failed to rollback on malformed braces.")
        
        # Metadata validation
        metadata = result.get('metadata', {})
        self.assertTrue(len(metadata.get('rollback_reasons', [])) > 0, "Missing rollback reason in metadata.")
        
    def test_broken_indentation_python(self):
        broken_py = "def foo():\nprint('bad')\n    pass\n"
        result = optimize_code(broken_py, 'python', [])
        self.assertEqual(result['code'], broken_py)
        
    def test_metadata_structure(self):
        """Verify the test metadata validation structure required by user."""
        code = "function test() { var x = 1; }"
        result = optimize_code(code, 'javascript', [])
        metadata = result.get('metadata', {})
        
        self.assertIn("applied_rules", metadata)
        self.assertIn("skipped_rules", metadata)
        self.assertIn("failed_rules", metadata)
        self.assertIn("rollback_reasons", metadata)
        
        if len(metadata['applied_rules']) > 0:
            rule_info = metadata['applied_rules'][0]
            self.assertIn("confidence", rule_info)
            self.assertIn("risk", rule_info)
