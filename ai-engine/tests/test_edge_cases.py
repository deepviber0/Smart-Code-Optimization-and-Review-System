import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimizer import optimize_code
from pipeline_validators import PipelineValidators

class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.samples_dir = os.path.join(os.path.dirname(__file__), 'samples')
        with open(os.path.join(self.samples_dir, 'js', 'messy.js'), 'r', encoding='utf-8') as f:
            self.messy_js = f.read()
        with open(os.path.join(self.samples_dir, 'python', 'messy.py'), 'r', encoding='utf-8') as f:
            self.messy_py = f.read()

    def test_messy_js_optimization(self):
        """Test messy JS async code with duplicates and unnecessary vars."""
        val = PipelineValidators('javascript')
        orig_funcs = val.count_functions(self.messy_js)
        
        result = optimize_code(self.messy_js, 'javascript', [{'rule_id': 'JS_BP_001'}])
        opt_code = result['code']
        
        # Verify function count remains same or decreases (if duplicate removed safely)
        new_funcs = val.count_functions(opt_code)
        self.assertTrue(new_funcs <= orig_funcs, "Function count increased unexpectedly.")
        
        # Verify async preservation
        self.assertIn("async function", opt_code)
        self.assertIn("await fetch", opt_code)
        
        # Check rule application
        self.assertTrue(len(result['metadata']['applied_rules']) > 0)
        
    def test_messy_python_optimization(self):
        """Test messy Python with bad exceptions, redundant code, and duplicate imports."""
        result = optimize_code(self.messy_py, 'python', [{'rule_id': 'PY_BP_003'}])
        opt_code = result['code']
        
        # Verify basic legacy rule fixes (e.g. exception handling)
        self.assertIn("except Exception as e:", opt_code)
        
        # Verify structural preservation
        self.assertIn("def calculate_something", opt_code)
        
    def test_large_file_timeout(self):
        """Test the performance protection against massive files."""
        large_code = "var x = 1;\n" * 60000 # Creates a file > 500KB
        result = optimize_code(large_code, 'javascript', [])
        self.assertEqual(result['code'], large_code)
        self.assertTrue(any("exceeds max optimization size" in r for r in result['metadata']['rollback_reasons']))

    def test_already_optimized_code(self):
        """Test that already optimized code doesn't get messed up or infinitely loop."""
        perfect_code = "function getFive() {\n    return 5;\n}\n"
        result = optimize_code(perfect_code, 'javascript', [])
        
        # Should not loop infinitely and should return similar code
        self.assertTrue("return 5" in result['code'])

    def test_duplicate_function_removal(self):
        """Test that exact duplicates are removed safely."""
        code = """
function hello() {
    console.log("world");
}

function hello() {
    console.log("world");
}
"""
        result = optimize_code(code, 'javascript', [])
        opt_code = result['code']
        self.assertEqual(opt_code.count("function hello"), 1, "Duplicate function was not removed.")
        
    def test_overloaded_functions_preservation(self):
        """Java/C++ overloading test: signatures differ, bodies identical. Should PRESERVE."""
        java_code = """
public class Test {
    public void print(int x) { System.out.println(x); }
    public void print(String x) { System.out.println(x); }
}
"""
        result = optimize_code(java_code, 'java', [])
        self.assertEqual(result['code'].count("public void print"), 2, "Overloaded methods were incorrectly removed.")

