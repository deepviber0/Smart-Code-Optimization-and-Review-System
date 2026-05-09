import sys
import os
sys.path.append(os.getcwd())
from optimizers.javascript import optimize_javascript

code = """
var x = 0;
function test() {
    return eval("1+1");
}
if (x == null) {
    document.body.innerHTML = "hi";
}
"""
issues = [
    {"rule_id": "JS_BP_001"},
    {"rule_id": "JS_BP_002"},
    {"rule_id": "JS_BP_003"},
    {"rule_id": "JS_CORR_003"},
]

optimized = optimize_javascript(code, issues)
print("--- OPTIMIZED CODE ---")
print(optimized)
