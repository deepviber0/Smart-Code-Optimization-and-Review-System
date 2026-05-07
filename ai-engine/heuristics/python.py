import re

def analyze_python(code, tree):
    issues = []
    steps = []
    
    if re.search(r'except\s*:', code):
        issues.append({
            "severity": "critical",
            "title": "Bare except clause",
            "description": "A bare 'except:' catches all exceptions, including SystemExit and KeyboardInterrupt."
        })
        steps.append({
            "number": 0,
            "what": "Specify exception type",
            "why": "Catching all exceptions can hide critical bugs and make debugging very difficult.",
            "how": "Change 'except:' to 'except Exception as e:' or catch a specific exception class."
        })
        
    if re.search(r'type\(.*?\)\s*==', code):
        issues.append({
            "severity": "warning",
            "title": "Using type() for comparison",
            "description": "Using type() == instead of isinstance() breaks inheritance patterns."
        })
        steps.append({
            "number": 0,
            "what": "Use isinstance()",
            "why": "isinstance() respects object inheritance, whereas type() == is too strict.",
            "how": "Replace 'type(x) == Y' with 'isinstance(x, Y)'."
        })
        
    return issues, steps
