import re
import os

def optimize_PY_CORR_001(code):
    # Fix mutable default argument: arg=[] -> arg=None
    pattern = r'def\s+(\w+)\s*\((.*?)(=\s*\[\s*\]|=\s*\{\s*\})(.*?)\)\s*:'
    def replace_def(match):
        func_name = match.group(1)
        args_before = match.group(2)
        args_after = match.group(4)
        arg_type = "[]" if "[" in match.group(3) else "{}"
        
        # Determine indentation of the next line
        indent_match = re.search(r'\n(\s+)', code[match.end():])
        indent = indent_match.group(1) if indent_match else "    "
        
        new_def = f"def {func_name}({args_before}=None{args_after}):\n{indent}# OPTIMIZED: PY_CORR_001 — Fixed mutable default argument\n{indent}if {args_before.split(',')[-1].strip()} is None: {args_before.split(',')[-1].strip()} = {arg_type}"
        return new_def

    # Simple version for single argument case
    code = re.sub(r'def\s+(\w+)\s*\(([\w_]+)\s*=\s*\[\s*\]\)\s*:', 
                  r'def \1(\2=None):\n    # OPTIMIZED: PY_CORR_001 — Fixed mutable default argument\n    if \2 is None: \2 = []', code)
    return code

def optimize_PY_BP_001(code):
    # Flag eval() usage
    if "eval(" in code:
        code = re.sub(r'(eval\(.*?\))', r'# OPTIMIZED: PY_BP_001 — Warning: eval() is dangerous\n\1', code)
    return code

def optimize_PY_BP_002(code):
    # Replace == None with is None
    new_code = re.sub(r'==\s*None', 'is None', code)
    if new_code != code:
        new_code = "# OPTIMIZED: PY_BP_002 — Used 'is None' for identity comparison\n" + new_code
    return new_code

def optimize_PY_BP_003(code):
    # Replace bare except with except Exception as e
    new_code = re.sub(r'except\s*:', 'except Exception as e:', code)
    if new_code != code:
        new_code = "# OPTIMIZED: PY_BP_003 — Replaced bare except with except Exception\n" + new_code
    return new_code

def optimize_PY_BP_004(code):
    # Replace hardcoded credentials
    pattern = r'(\w*(?:password|passwd|secret|token|api_key)\w*\s*=\s*)(["\'].*?["\'])'
    def replace_cred(match):
        prefix = match.group(1)
        return f'{prefix}os.environ.get("SECRET_KEY") # OPTIMIZED: PY_BP_004 — Removed hardcoded credential'
    
    return re.sub(pattern, replace_cred, code, flags=re.IGNORECASE)

def optimize_PY_PERF_001(code):
    # Suggest join() for string concatenation in loop (Comment only as full rewrite is complex)
    if "+=" in code and ("for " in code or "while " in code):
        return "# OPTIMIZED: PY_PERF_001 — Consider using ''.join() for string concatenation in loops\n" + code
    return code

def optimize_PY_PERF_002(code):
    # Replace range(len(x)) with enumerate(x)
    pattern = r'for\s+(\w+)\s+in\s+range\s*\(\s*len\s*\(\s*(\w+)\s*\)\s*\)\s*:'
    replacement = r'for \1, _item in enumerate(\2): # OPTIMIZED: PY_PERF_002 — Used enumerate() instead of range(len())'
    return re.sub(pattern, replacement, code)

def optimize_PY_READ_001(code):
    # Flag long functions
    lines = code.split('\n')
    optimized_lines = []
    in_func = False
    func_start = 0
    
    for i, line in enumerate(lines):
        if line.strip().startswith("def "):
            in_func = True
            func_start = i
        elif in_func and (not line.startswith(" ") and line.strip()):
            if i - func_start > 50:
                lines[func_start] = "# OPTIMIZED: PY_READ_001 — Function over 50 lines, consider refactoring\n" + lines[func_start]
            in_func = False
    return '\n'.join(lines)

def optimize_python(code, issues):
    optimized_code = code
    # Sort issues to avoid overlapping replacements if needed, but here we just chain
    rule_map = {
        "PY_CORR_001": optimize_PY_CORR_001,
        "PY_BP_001": optimize_PY_BP_001,
        "PY_BP_002": optimize_PY_BP_002,
        "PY_BP_003": optimize_PY_BP_003,
        "PY_BP_004": optimize_PY_BP_004,
        "PY_PERF_001": optimize_PY_PERF_001,
        "PY_PERF_002": optimize_PY_PERF_002,
        "PY_READ_001": optimize_PY_READ_001,
    }
    
    applied_rules = set()
    for issue in issues:
        rule_id = issue.get("rule_id")
        if rule_id in rule_map and rule_id not in applied_rules:
            optimized_code = rule_map[rule_id](optimized_code)
            applied_rules.add(rule_id)
            
    return optimized_code
