import re

def analyze_c_cpp(code, tree, language):
    issues = []
    steps = []
    
    if re.search(r'\bgets\s*\(', code):
        issues.append({
            "severity": "critical",
            "title": "Dangerous function 'gets' used",
            "description": "The gets() function is unsafe and can cause buffer overflow vulnerabilities."
        })
        steps.append({
            "number": 0,
            "what": "Replace gets()",
            "why": "gets() does not check the bounds of the destination buffer, leading to extreme security risks.",
            "how": "Use fgets() instead, specifying the buffer size."
        })
        
    if re.search(r'\bmalloc\s*\(', code) and 'free' not in code:
        issues.append({
            "severity": "warning",
            "title": "Possible memory leak",
            "description": "Memory is allocated using malloc() but never explicitly freed."
        })
        steps.append({
            "number": 0,
            "what": "Free allocated memory",
            "why": "Unfreed memory causes the application memory usage to grow indefinitely.",
            "how": "Ensure every malloc() has a corresponding free() when the memory is no longer needed."
        })

    return issues, steps
