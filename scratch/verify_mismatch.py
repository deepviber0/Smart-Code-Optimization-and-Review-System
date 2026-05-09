import requests
import json

def test_mismatch():
    url = "http://localhost:5002/api/analyze"
    
    # JavaScript code
    js_code = """
    function calculate(x, y) {
        let result = x + y;
        if (result === 10) {
            console.log("Ten!");
        }
        return result;
    }
    """
    
    # Payload with INCORRECT language (C)
    payload = {
        "code": js_code,
        "language": "c"
    }
    
    print(f"Sending JS code with 'C' selected to {url}...")
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        print("\n--- RESULTS ---")
        print(f"Overall Score: {data['score']['overall']}")
        print(f"Detected Language: {data['metadata']['detected_language']}")
        print(f"Detection Confidence: {data['metadata']['detection_confidence']}")
        print(f"Original Selection: {data['metadata']['original_selection']}")
        
        issues = data['issues']
        mismatch_found = any(i['rule_id'] == 'LANG_MISMATCH' for i in issues)
        print(f"Mismatch Issue Found: {mismatch_found}")
        
        if mismatch_found:
            for i in issues:
                if i['rule_id'] == 'LANG_MISMATCH':
                    print(f"Issue Severity: {i['severity']}")
                    print(f"Issue Title: {i['title']}")
                    print(f"Issue Description: {i['description']}")
        
        if data['score']['overall'] < 20 and mismatch_found and data['metadata']['detected_language'] == 'javascript':
            print("\n✅ TEST PASSED: System correctly identified the mismatch and penalized the score.")
        else:
            print("\n❌ TEST FAILED: System did not handle the mismatch as expected.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_mismatch()
