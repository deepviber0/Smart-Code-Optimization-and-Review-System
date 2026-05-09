import re

def optimize_JS_BP_001(code):
    # Replace var with let
    new_code = re.sub(r'\bvar\b', 'let', code)
    if new_code != code:
        new_code = "// OPTIMIZED: JS_BP_001 — Replaced 'var' with 'let' for better scoping\n" + new_code
    return new_code

def optimize_JS_BP_002(code):
    # Flag eval() - Keep on same line but add comment above
    pattern = r'(^.*eval\(.*?\).*$)'
    replacement = r'// OPTIMIZED: JS_BP_002 — Warning: eval() is a security risk\n\1'
    return re.sub(pattern, replacement, code, flags=re.MULTILINE)

def optimize_JS_BP_003(code):
    # Replace innerHTML with textContent
    return re.sub(r'(\.innerHTML\s*=\s*)', r'.textContent = /* OPTIMIZED: JS_BP_003 — Replaced innerHTML with textContent */ ', code)

def optimize_JS_BP_004(code):
    # Add missing semicolons (basic regex)
    lines = code.split('\n')
    optimized_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.endswith((';', '{', '}', ',', '[')) and not stripped.startswith(('//', '/*', '*', 'if', 'for', 'while', 'function')):
            optimized_lines.append(line + "; // OPTIMIZED: JS_BP_004 — Added missing semicolon")
        else:
            optimized_lines.append(line)
    return '\n'.join(optimized_lines)

def optimize_JS_CORR_001(code):
    # Add let to undeclared loop variable
    pattern = r'for\s*\(\s*(\w+)\s*=\s*0\s*;'
    replacement = r'for (let \1 = 0; // OPTIMIZED: JS_CORR_001 — Declared loop variable with let'
    return re.sub(pattern, replacement, code)

def optimize_JS_CORR_002(code):
    # Replace == with === (Avoid matching === or already replaced ones)
    return re.sub(r'(?<!=)==(?!=)', r'=== /* OPTIMIZED: JS_CORR_002 — Used strict equality */ ', code)

def optimize_JS_CORR_003(code):
    # Replace == null with === null (Avoid matching === null)
    return re.sub(r'(?<!=)==\s*null', r'=== null /* OPTIMIZED: JS_CORR_003 — Used strict null check */ ', code)

def optimize_JS_PERF_001(code):
    # Move console.log outside loop (comment suggestion)
    if "console.log" in code and ("for" in code or "while" in code):
        return "// OPTIMIZED: JS_PERF_001 — Move console.log outside the loop to improve performance\n" + code
    return code

def optimize_javascript(code, issues):
    optimized_code = code
    rule_map = {
        "JS_BP_001": optimize_JS_BP_001,
        "JS_BP_002": optimize_JS_BP_002,
        "JS_BP_003": optimize_JS_BP_003,
        "JS_BP_004": optimize_JS_BP_004,
        "JS_CORR_001": optimize_JS_CORR_001,
        "JS_CORR_002": optimize_JS_CORR_002,
        "JS_CORR_003": optimize_JS_CORR_003,
        "JS_PERF_001": optimize_JS_PERF_001,
    }
    
    applied_rules = set()
    for issue in issues:
        rule_id = issue.get("rule_id")
        if rule_id in rule_map and rule_id not in applied_rules:
            optimized_code = rule_map[rule_id](optimized_code)
            applied_rules.add(rule_id)
            
    return optimized_code
