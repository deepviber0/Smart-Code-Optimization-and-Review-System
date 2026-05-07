import re

def analyze_javascript(code, tree):
    issues = []
    steps = []
    
    if 'var ' in code:
        issues.append({
            "severity": "warning",
            "title": "Use of 'var'",
            "description": "Use 'let' or 'const' instead of 'var' for block scoping."
        })
        steps.append({
            "number": 0,
            "what": "Replace 'var' declarations",
            "why": "'var' has function-level scope and can lead to variable hoisting bugs.",
            "how": "Change 'var' to 'let' or 'const'."
        })

    if 'console.log' in code and 'for' in code:
        # A simple string search to see if console.log is inside a loop loosely
        if re.search(r'for\s*\(.*?\)\s*\{[^\}]*console\.log', code, re.DOTALL):
            issues.append({
                "severity": "warning",
                "title": "Console.log in loop",
                "description": "Printing inside a loop is inefficient."
            })
            steps.append({
                "number": 0,
                "what": "Remove or batch console.log calls",
                "why": "I/O operations in a loop can cause massive performance bottlenecks.",
                "how": "Store results in an array and print outside the loop."
            })

    if re.search(r'for\s*\(\s*[a-zA-Z]+\s*=', code) and not re.search(r'for\s*\(\s*(let|var|const)\s+[a-zA-Z]+\s*=', code):
        issues.append({
            "severity": "critical",
            "title": "Undeclared loop variable",
            "description": "Loop counter is implicitly declared globally."
        })
        steps.append({
            "number": 0,
            "what": "Declare loop counter",
            "why": "Global loop counters can overwrite variables elsewhere and cause hard-to-track bugs.",
            "how": "Add 'let' before your loop variable."
        })
        
    if '==' in code and '===' not in code:
        issues.append({
            "severity": "warning",
            "title": "Loose Equality Used",
            "description": "Using '==' instead of '===' can cause unexpected type coercion."
        })
        steps.append({
            "number": 0,
            "what": "Use Strict Equality",
            "why": "Strict equality ('===') compares both value and type, preventing subtle bugs.",
            "how": "Replace '==' with '==='."
        })

    return issues, steps
