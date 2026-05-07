def analyze_base(code, tree):
    issues = []
    steps = []
    
    # Simple check for empty blocks
    if '{}' in code.replace(' ', '').replace('\n', ''):
        issues.append({
            "severity": "warning",
            "title": "Empty block detected",
            "description": "Empty blocks of code are often a sign of unfinished logic or can cause confusion."
        })
        steps.append({
            "number": 0,
            "what": "Remove or fill empty block",
            "why": "Empty brackets add dead space and make code harder to maintain.",
            "how": "Either add the missing logic inside the block, or remove the block entirely."
        })
        
    return issues, steps
