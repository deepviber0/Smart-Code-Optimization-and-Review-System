import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimizer import optimize_code

class TestMultiLanguagePipeline(unittest.TestCase):
    
    def test_js_rules_isolation(self):
        """Ensure JS rules (var -> let) do not apply to Python code."""
        python_code = "var = 10\ndef foo():\n    pass"
        result = optimize_code(python_code, 'python', [{'rule_id': 'JS_BP_001'}])
        # 'var' should not become 'let' in python
        self.assertIn("var = 10", result['code'])
        self.assertNotIn("let = 10", result['code'])

    def test_c_cpp_macros(self):
        """Ensure C/C++ macros are untouched."""
        c_code = "#include <stdio.h>\n#define CONST_VAR 100\nvoid foo() { int var = 1; }"
        result = optimize_code(c_code, 'c', [])
        self.assertIn("#define CONST_VAR 100", result['code'])

    def test_java_class_structure(self):
        """Test Java classes with annotations."""
        java_code = "@Override\npublic class Foo {\n    public void bar() {}\n}"
        result = optimize_code(java_code, 'java', [])
        self.assertIn("@Override", result['code'])
        self.assertIn("public class Foo", result['code'])

    def test_string_masking_preservation(self):
        """Ensure strings are not corrupted by regex replacements."""
        # JS rule: \bvar\b -> let
        # If masking works, this string shouldn't change
        js_code = 'var x = "var my_var = 1;";\n'
        result = optimize_code(js_code, 'javascript', [{'rule_id': 'JS_BP_001'}])
        
        # The actual code 'var x' should become 'let x', but string 'var my_var' shouldn't
        self.assertIn('let x =', result['code'])
        self.assertIn('"var my_var = 1;"', result['code'])
        
    def test_python_indentation_preservation(self):
        """Ensure Python indentation isn't corrupted."""
        py_code = "def test():\n    if True:\n        print('Hello')\n    return 0\n"
        result = optimize_code(py_code, 'python', [])
        lines = result['code'].split('\n')
        
        # Check that the print statement still has 8 spaces
        has_correct_indent = any(line.startswith("        print") for line in lines)
        self.assertTrue(has_correct_indent, "Python indentation was corrupted.")

