import re

def analyze_java(code, tree):
    issues = []
    steps = []
    
    if re.search(r'catch\s*\([^)]+\)\s*\{\s*\}', code):
        issues.append({
            "severity": "critical",
            "title": "Empty catch block",
            "description": "Catching an exception without handling it swallows the error silently."
        })
        steps.append({
            "number": 0,
            "what": "Handle the exception",
            "why": "Silent failures make applications unpredictable and very hard to debug.",
            "how": "At a minimum, log the error using a logger or print stack trace."
        })
        
    if '==' in code and '.equals(' not in code and 'String' in code:
        issues.append({
            "severity": "warning",
            "title": "Possible String comparison with ==",
            "description": "Using '==' to compare strings compares object references, not values."
        })
        steps.append({
            "number": 0,
            "what": "Use .equals() for objects",
            "why": "'==' checks memory location. Strings with the same value might live in different memory locations.",
            "how": "Change 'str1 == str2' to 'str1.equals(str2)'."
        })
        
    return issues, steps
