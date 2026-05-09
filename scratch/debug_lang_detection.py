import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai-engine')))

from language_detector import detect_language_ast, validate_language, compute_fingerprint_score, collect_node_types
from ast_parser import parse_code

py_code = """
def hello(x=[]):
    if x is None:
        print("world")
    return x
"""

print("--- TESTING PYTHON CODE ---")
best_lang, best_score = detect_language_ast(py_code)
print(f"Best detected: {best_lang} with score {best_score}")

# Check JS score for this code
tree, conf, err = parse_code(py_code, 'javascript')
if tree:
    node_types = collect_node_types(tree)
    fp_score = compute_fingerprint_score(node_types, 'javascript')
    sel_score = 0.4 * conf + 0.6 * fp_score
    print(f"JS score for PY code: {sel_score} (Conf: {conf}, FP: {fp_score})")
    # print(f"Node types detected in JS parse: {node_types}")

issue, corrected = validate_language(py_code, 'javascript')
print(f"Validation result: Issue={issue is not None}, Corrected={corrected}")
