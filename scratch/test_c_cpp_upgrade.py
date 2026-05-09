import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai-engine')))

from heuristics.c_cpp import analyze_c_cpp
from optimizers.c_cpp import optimize_c_cpp

test_code = """
#include <stdio.h>
#include <string.h>

void bad_func(char* userInput) {
    char buf[10];
    gets(buf);
    
    char dest[20];
    strcpy(dest, "Constant string is fine");
    strcpy(dest, userInput);
    
    printf(userInput);
    
    for (int i = 0; i < 10; i++) {
        void* p = malloc(1024);
    }
}
"""

print("--- ANALYZING CODE (C) ---")
issues, steps = analyze_c_cpp(test_code, language="c")
for issue in issues:
    print(f"[{issue['rule_id']}] {issue['severity'].upper()}: {issue['title']} at line {issue['line']}")
    print(f"    {issue['description']}")

print("\n--- OPTIMIZING CODE (C) ---")
result = optimize_c_cpp(test_code, language="c")
print(result['optimized_code'])
