import re

def optimize_JS_BP_001(code):
    return re.sub(r'\bvar\b', 'let', code)

def optimize_JS_BP_002(code):
    return code # Handled in metadata only

def optimize_JS_BP_003(code):
    return re.sub(r'(\.innerHTML\s*=\s*)', r'.textContent = ', code)

def optimize_JS_BP_004(code):
    return code # Dangerous generic heuristic removed

def optimize_JS_CORR_001(code):
    pattern = r'for\s*\(\s*(\w+)\s*=\s*0\s*;'
    replacement = r'for (let \1 = 0;'
    return re.sub(pattern, replacement, code)

def optimize_JS_CORR_002(code):
    return re.sub(r'(?<!=)==(?!=)', r'===', code)

def optimize_JS_CORR_003(code):
    return re.sub(r'(?<!=)==\s*null', r'=== null', code)

def optimize_JS_PERF_001(code):
    return code # Handled by DeepOptimizer now

def optimize_javascript(code, issues, global_applied_rules=None):
    if global_applied_rules is None:
        global_applied_rules = set()
    
    optimized_code = code
    rule_map = {
        "JS_BP_001": ("Variable Scoping", optimize_JS_BP_001),
        "JS_BP_002": ("Security Fix", optimize_JS_BP_002),
        "JS_BP_003": ("DOM Optimization", optimize_JS_BP_003),
        "JS_BP_004": ("Semicolon Injection", optimize_JS_BP_004),
        "JS_CORR_001": ("Loop Declaration", optimize_JS_CORR_001),
        "JS_CORR_002": ("Strict Equality", optimize_JS_CORR_002),
        "JS_CORR_003": ("Null Safety", optimize_JS_CORR_003),
    }
    
    for issue in issues:
        rule_id = issue.get("rule_id")
        if rule_id in rule_map and rule_id not in global_applied_rules:
            desc, func = rule_map[rule_id]
            optimized_code = func(optimized_code)
            global_applied_rules.add(rule_id)
            
    return optimized_code
