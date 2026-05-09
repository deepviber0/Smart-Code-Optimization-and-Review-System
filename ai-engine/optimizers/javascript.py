import re

def optimize_JS_BP_001(code):
    return re.sub(r'\bvar\b', 'let', code)

def optimize_JS_BP_002(code):
    return re.sub(r'(^.*eval\(.*?\).*$)', r'// Warning: eval() is a security risk\n\1', code, flags=re.MULTILINE)

def optimize_JS_BP_003(code):
    return re.sub(r'(\.innerHTML\s*=\s*)', r'.textContent = ', code)

def optimize_JS_BP_004(code):
    lines = code.split('\n')
    optimized_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.endswith((';', '{', '}', ',', '[')) and not stripped.startswith(('//', '/*', '*', 'if', 'for', 'while', 'function')):
            optimized_lines.append(line + ";")
        else:
            optimized_lines.append(line)
    return '\n'.join(optimized_lines)

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

def optimize_javascript(code, issues):
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
    
    applied_descriptions = []
    applied_rules = set()
    for issue in issues:
        rule_id = issue.get("rule_id")
        if rule_id in rule_map and rule_id not in applied_rules:
            desc, func = rule_map[rule_id]
            optimized_code = func(optimized_code)
            applied_descriptions.append(desc)
            applied_rules.add(rule_id)
            
    if applied_descriptions:
        header = f"// Optimized: {', '.join(applied_descriptions)}\n"
        return header + optimized_code
        
    return optimized_code
