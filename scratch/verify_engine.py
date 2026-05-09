import requests
import json

def test_analyze(code, language):
    url = "http://localhost:5001/analyze"
    payload = {
        "code": code,
        "language": language
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def verify_case(name, code, selected_lang, expected_lang=None):
    print(f"\n--- Testing: {name} ---")
    result = test_analyze(code, selected_lang)
    
    if "error" in result:
        print(f"FAILED: {result['error']}")
        return

    detected_lang = result.get("language")
    print(f"Selected: {selected_lang}, Detected/Used: {detected_lang}")
    
    if expected_lang and detected_lang != expected_lang:
        print(f"FAILURE: Expected {expected_lang} but got {detected_lang}")
    else:
        print("SUCCESS: Language match/correction correct.")

    opt_code = result.get("optimizedCode", "")
    print(f"Optimizations found: {len(result.get('issues', []))} issues, {len(result.get('steps', []))} steps")
    # print(f"First 100 chars of optimized code: {opt_code[:100]}...")

# 1. Python code mislabeled as JS
python_code = """
def calculate_sum(n):
    total = 0
    for i in range(n):
        total += i
    return total
"""

# 2. JS code mislabeled as Python
js_code = """
function calculateSum(n) {
    let total = 0;
    for (let i = 0; i < n; i++) {
        total += i;
    }
    return total;
}
"""

# 3. Java code
java_code = """
package com.example;
public class Main {
    public static void main(String[] args) {
        String s = "hello";
        if (s == "world") {
            System.out.println("Match");
        }
    }
}
"""

# 4. C++ code with NULL
cpp_code = """
#include <iostream>
void foo(int* p) {
    if (p == NULL) {
        return;
    }
}
"""

if __name__ == "__main__":
    print("Starting Verification...")
    
    # Test cases
    verify_case("Python mislabeled as JS", python_code, "javascript", "python")
    verify_case("JS mislabeled as Python", js_code, "python", "javascript")
    verify_case("Python correctly labeled", python_code, "python", "python")
    verify_case("Java with string == and println", java_code, "java", "java")
    verify_case("C++ with NULL", cpp_code, "cpp", "cpp")
