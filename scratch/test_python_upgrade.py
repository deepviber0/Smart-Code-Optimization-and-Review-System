import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai-engine')))

from heuristics.python import analyze_python
from optimizers.python import optimize_python

test_code = """
import pickle
import subprocess

def bad_func(x=[]):
    if x == None:
        print("x is None")
    
    res = ""
    for i in range(len(range(10))):
        res += str(i)
        
    eval("print('danger')")
    subprocess.run("ls", shell=True)
    
    items = [1, 2, 3]
    for item in items:
        if item == 2:
            items.remove(item)
            
    return res

class MySubClass:
    def __init__(self):
        # Missing super().__init__()
        self.val = 10
"""

print("--- ANALYZING CODE ---")
issues = analyze_python(test_code)
for issue in issues:
    print(f"[{issue['rule_id']}] {issue['severity'].upper()}: {issue['title']} at line {issue['line']}")
    print(f"    {issue['description']}")

print("\n--- OPTIMIZING CODE ---")
result = optimize_python(test_code)
print(result['optimized_code'])
