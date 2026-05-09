import re
import os

def optimize_PY_CORR_001(code):
    code = re.sub(r'def\s+(\w+)\s*\(([\w_]+)\s*=\s*\[\s*\]\)\s*:', 
                  r'def \1(\2=None):\n    if \2 is None: \2 = []', code)
    return code

def optimize_PY_BP_001(code):
    return re.sub(r'(eval\(.*?\))', r'# Warning: eval() is dangerous\n\1', code)

def optimize_PY_BP_002(code):
    return re.sub(r'==\s*None', 'is None', code)

def optimize_PY_BP_003(code):
    return re.sub(r'except\s*:', 'except Exception as e:', code)

def optimize_PY_BP_004(code):
    pattern = r'(\w*(?:password|passwd|secret|token|api_key)\w*\s*=\s*)(["\'].*?["\'])'
    def replace_cred(match):
        prefix = match.group(1)
        return f'{prefix}os.environ.get("SECRET_KEY")'
    return re.sub(pattern, replace_cred, code, flags=re.IGNORECASE)

def optimize_PY_PERF_001(code):
    return code # Handled by DeepOptimizer

def optimize_PY_PERF_002(code):
    pattern = r'for\s+(\w+)\s+in\s+range\s*\(\s*len\s*\(\s*(\w+)\s*\)\s*\)\s*:'
    replacement = r'for \1, _item in enumerate(\2):'
    return re.sub(pattern, replacement, code)

def optimize_PY_READ_001(code):
    return code # Informational only

def optimize_python(code, issues):
    optimized_code = code
    rule_map = {
        "PY_CORR_001": ("Mutable Default Fix", optimize_PY_CORR_001),
        "PY_BP_001": ("Security Fix", optimize_PY_BP_001),
        "PY_BP_002": ("Identity Comparison", optimize_PY_BP_002),
        "PY_BP_003": ("Exception Handling", optimize_PY_BP_003),
        "PY_BP_004": ("Secret Management", optimize_PY_BP_004),
        "PY_PERF_002": ("Enumerate Usage", optimize_PY_PERF_002),
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
        header = f"# Optimized: {', '.join(applied_descriptions)}\n"
        return header + optimized_code
        
    return optimized_code
