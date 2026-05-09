import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai-engine')))

from heuristics.javascript import analyze_javascript
from optimizers.javascript import optimize_javascript

test_code = """
var x = 10;
if (x == "10") {
    console.log("Loose equality");
}

for (i = 0; i < 10; i++) {
    console.log(i);
    document.getElementById("test").innerHTML = i;
}

function bad() {
    eval("alert('hack')");
    document.write("Don't use this");
    
    if (x == null) {
        console.log("x is null");
    }
    
    if (x === NaN) {
        console.log("This will never be true");
    }
}
"""

print("--- ANALYZING CODE ---")
issues, steps = analyze_javascript(test_code)
for issue in issues:
    print(f"[{issue['rule_id']}] {issue['severity'].upper()}: {issue['title']} at line {issue['line']}")
    print(f"    {issue['description']}")

print("\n--- OPTIMIZING CODE ---")
result = optimize_javascript(test_code)
print(result['optimized_code'])
