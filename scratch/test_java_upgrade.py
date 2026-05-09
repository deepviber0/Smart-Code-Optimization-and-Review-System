import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai-engine')))

from heuristics.java import analyze_java
from optimizers.java import optimize_java

test_code = """
public class Test {
    public void method() {
        try {
            int x = 10;
        } catch (Exception e) {
            // Empty
        }
        
        String s = "hello";
        if (s == "hello") {
            System.out.println("Match");
        }
        
        for (int i = 0; i < 10; i++) {
            s += i;
            Object obj = new Object();
        }
        
        FileInputStream fis = new FileInputStream("test.txt");
    }
}
"""

print("--- ANALYZING CODE ---")
issues, steps = analyze_java(test_code)
for issue in issues:
    print(f"[{issue['rule_id']}] {issue['severity'].upper()}: {issue['title']} at line {issue['line']}")
    print(f"    {issue['description']}")

print("\n--- OPTIMIZING CODE ---")
result = optimize_java(test_code)
print(result['optimized_code'])
