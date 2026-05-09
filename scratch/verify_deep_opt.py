import requests
import json

def test_optimization(code, language):
    url = "http://localhost:5001/analyze"
    payload = {
        "code": code,
        "language": language
    }
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        
        print(f"\n--- Testing {language.upper()} Optimization ---")
        print(f"Score: {result['score']['overall']}")
        print(f"Explanation: {result['explanation']}")
        print(f"Metadata: {json.dumps(result['metadata'], indent=2)}")
        print("\nOptimized Code Snippet (First 5 lines):")
        print("\n".join(result['optimizedCode'].split('\n')[:5]))
        
        # Check for specific performance issues in results
        issues = [i['title'] for i in result['issues']]
        print(f"Issues Found: {', '.join(issues)}")
        
        return result
    except Exception as e:
        print(f"Error testing {language}: {e}")
        return None

# Test Case 1: JavaScript Nested Loop (O(n^2))
js_code = """
function findDuplicates(arr) {
    for (var i = 0; i < arr.length; i++) {
        for (var j = i + 1; j < arr.length; j++) {
            if (arr[i] === arr[j]) {
                console.log("Duplicate found: " + arr[i]);
            }
        }
    }
}
"""

# Test Case 2: Python Repeated Calculation in Loop
py_code = """
def calculate_sums(items):
    results = []
    for item in items:
        # Redundant calculation inside loop
        factor = 10 * 5 / 2 + 100
        results.append(item * factor)
        print("Processed item: " + str(item))
    return results
"""

if __name__ == "__main__":
    print("Starting Deep Optimization System Verification...")
    test_optimization(js_code, "javascript")
    test_optimization(py_code, "python")
