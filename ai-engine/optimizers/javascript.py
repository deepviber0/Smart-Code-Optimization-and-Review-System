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

def optimize_JS_FMT_001(code):
    """Normalize operator spacing: a+b -> a + b"""
    # 1. Spacing around comparison/arithmetic operators
    # This avoids i++ by checking for single operators surrounded by word chars
    code = re.sub(r'(\w+)([\+\-\*\/\|\&\>\<])(\w+)', r'\1 \2 \3', code)
    # 2. Spacing around assignment
    code = re.sub(r'(?<=\w)=([^=])', r' = \1', code) # Fix assignment spacing
    # 3. Clean up double spaces if any
    code = re.sub(r' +', ' ', code)
    # 4. Spacing after keywords
    code = re.sub(r'\b(if|for|while|switch|catch)\s*\(', r'\1 (', code)
    # 5. Spacing in for loops (after semicolons)
    code = re.sub(r';(\S)', r'; \1', code)
    return code

def optimize_JS_FMT_002(code):
    """Combine declaration and assignment: let x; x = 5; -> const x = 5;"""
    # Robust multi-line match for let/var followed by assignment
    pattern = r'(?:let|var)\s+(\w+)\s*;?\s*\n\s*\1\s*=\s*([^;\n]+);?'
    replacement = r'const \1 = \2;'
    return re.sub(pattern, replacement, code)

def optimize_javascript(code, issues, global_applied_rules=None):
    if global_applied_rules is None:
        global_applied_rules = set()
    
    optimized_code = code
    rule_map = {
        "JS_BP_001": ("Variable Scoping", optimize_JS_BP_001),
        "JS_BP_002": ("Security Fix", optimize_JS_BP_002),
        "JS_BP_003": ("DOM Optimization", optimize_JS_BP_003),
        "JS_CORR_001": ("Loop Declaration", optimize_JS_CORR_001),
        "JS_CORR_002": ("Strict Equality", optimize_JS_CORR_002),
        "JS_CORR_003": ("Null Safety", optimize_JS_CORR_003),
    }
    
    # 1. Apply structural/legacy rules
    for issue in issues:
        rule_id = issue.get("rule_id")
        if rule_id in rule_map and rule_id not in global_applied_rules:
            desc, func = rule_map[rule_id]
            optimized_code = func(optimized_code)
            global_applied_rules.add(rule_id)
            
    # 2. Apply formatting cleanup (always)
    optimized_code = optimize_JS_FMT_002(optimized_code)
    optimized_code = optimize_JS_FMT_001(optimized_code)
            
    return optimized_code
